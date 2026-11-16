<script setup>
import { ref, nextTick, computed } from 'vue'
import { marked } from 'marked'
import DOMPurify from 'dompurify'

// Config marked : tableaux + retours à la ligne simples pris en compte
marked.setOptions({
  breaks: true,
  gfm: true
})

/**
 * Convertit le Markdown renvoyé par le LLM (titres, tableaux, gras, listes...)
 * en HTML propre et sécurisé, prêt à être injecté via v-html.
 */
function renderMarkdown(text) {
  if (!text) return ''
  const rawHtml = marked.parse(text)
  return DOMPurify.sanitize(rawHtml)
}

const question = ref('')
const messages = ref([])
const loading = ref(false)
const error = ref('')
const textareaRef = ref(null)
const messagesEndRef = ref(null)

const MAX_LENGTH = 2000
const charCount = computed(() => question.value.length)

const GREETING = 'Bonjour 👋 Je suis LogAI, votre assistant d\'analyse de logs réseau. Comment puis-je vous aider aujourd\'hui ?'

const EXAMPLES = [
  { icon: '🔍', text: 'Pourquoi cette erreur apparaît ?' },
  { icon: '📖', text: 'Que signifie cette erreur ?' },
  { icon: '⚠️', text: 'Quelles sont les causes possibles ?' },
  { icon: '🛠️', text: 'Que dois-je faire pour résoudre ce problème ?' }
]

function autoResize() {
  const el = textareaRef.value
  if (!el) return
  el.style.height = 'auto'
  el.style.height = Math.min(el.scrollHeight, 160) + 'px'
}

function scrollToBottom() {
  nextTick(() => {
    messagesEndRef.value?.scrollIntoView({ behavior: 'smooth', block: 'end' })
  })
}

function handleKeydown(e) {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault()
    sendMessage()
  }
}

async function sendMessage() {
  const text = question.value.trim()

  if (!text || loading.value) {
    return
  }

  messages.value.push({
    role: 'user',
    content: text
  })

  question.value = ''
  error.value = ''
  loading.value = true

  nextTick(() => autoResize())
  scrollToBottom()

  try {
    const response = await fetch('http://localhost:8001/chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        question: text
      })
    })

    if (!response.ok) {
      throw new Error(`Erreur HTTP ${response.status}`)
    }

    const data = await response.json()

    console.log('Réponse backend :', data)

    messages.value.push({
      role: 'assistant',

      // Réponse principale
      content:
        data.response ||
        data.answer ||
        'Aucune réponse reçue du serveur.',

      // Informations structurées optionnelles
      analysis: data.analysis || null,
      meaning: data.meaning || null,
      causes: data.causes || [],
      actions: data.actions || [],
      severity: data.severity || null,
      confidence: data.confidence || null,
      sources: data.sources || [],
      template: data.template || null,
      incident: data.incident || null
    })

  } catch (err) {
    console.error('Erreur:', err)

    error.value =
      'Impossible de contacter le serveur FastAPI. Vérifie que l\u2019API fonctionne sur le port 8001.'
  } finally {
    loading.value = false
    scrollToBottom()
  }
}

function askExample(text) {
  question.value = text
  nextTick(() => {
    autoResize()
    textareaRef.value?.focus()
  })
}

function clearInput() {
  question.value = ''
  nextTick(() => autoResize())
}
</script>


<template>

  <div class="app">

    <!-- =====================================================
         HEADER
    ====================================================== -->

    <header class="header">

      <div class="header-content">

        <div class="logo">
          🤖
        </div>

        <div>
          <h1>LogAI Assistant</h1>
          <p>Analyse intelligente des logs réseau</p>
        </div>

        <div class="status">
          <span class="status-dot"></span>
          API connectée
        </div>

      </div>

    </header>


    <!-- =====================================================
         CHAT
    ====================================================== -->

    <main class="chat-container">

      <!-- ================= MESSAGE DE BIENVENUE (bulle de chat) ================= -->

      <div
        v-if="messages.length === 0"
        class="message assistant"
      >

        <div class="avatar">
          🤖
        </div>

        <div class="assistant-content">

          <div class="assistant-header">
            <div class="message-role">
              LogAI
            </div>
          </div>

          <section class="response-card main-response greeting-card">

            <div class="response-text">
              {{ GREETING }}
            </div>

          </section>

          <div class="examples">

            <button
              v-for="(example, index) in EXAMPLES"
              :key="index"
              @click="askExample(example.text)"
            >
              <span>{{ example.icon }}</span>
              {{ example.text }}
            </button>

          </div>

        </div>

      </div>


      <!-- ================= MESSAGES ================= -->

      <div class="messages">

        <div
          v-for="(message, index) in messages"
          :key="index"
          class="message"
          :class="message.role"
        >

          <!-- AVATAR -->

          <div class="avatar">

            <span v-if="message.role === 'user'">
              👤
            </span>

            <span v-else>
              🤖
            </span>

          </div>


          <!-- ================= USER ================= -->

          <div
            v-if="message.role === 'user'"
            class="message-content user-content"
          >

            <div class="message-role">
              Vous
            </div>

            <div class="message-text">
              {{ message.content }}
            </div>

          </div>


          <!-- ================= ASSISTANT ================= -->

          <div
            v-else
            class="assistant-content"
          >

            <!-- En-tête : nom + badges de statut regroupés (confiance + sévérité) -->

            <div class="assistant-header">

              <div class="message-role">
                LogAI
              </div>

              <div class="status-badges">

                <span
                  v-if="message.severity"
                  class="severity"
                  :class="String(message.severity).toLowerCase()"
                >
                  {{ message.severity }}
                </span>

                <span
                  v-if="message.confidence !== null"
                  class="confidence"
                >
                  RAG : {{ Math.round(message.confidence * 100) }}%
                </span>

              </div>

            </div>


            <!-- ================= 1. RÉPONSE PRINCIPALE ================= -->

            <section class="response-card main-response">

              <div class="section-title">
                <span>💡</span>
                Réponse
              </div>

              <div
                class="response-text markdown-body"
                v-html="renderMarkdown(message.content)"
              ></div>

            </section>


            <!-- ================= 2. TEMPLATE DÉTECTÉ ================= -->

            <section
              v-if="message.template"
              class="response-card"
            >

              <div class="section-title">
                <span>🧩</span>
                Template détecté
              </div>

              <div class="template-box">
                {{ message.template }}
              </div>

            </section>


            <!-- ================= 3. COMPRÉHENSION (signification + analyse fusionnées) ================= -->

            <section
              v-if="message.meaning || message.analysis"
              class="response-card"
            >

              <div
                v-if="message.meaning"
                class="sub-block"
              >

                <div class="section-title">
                  <span>📖</span>
                  Signification
                </div>

                <div
                  class="markdown-body"
                  v-html="renderMarkdown(message.meaning)"
                ></div>

              </div>

              <div
                v-if="message.analysis"
                class="sub-block"
                :class="{ 'sub-block-divider': message.meaning }"
              >

                <div class="section-title">
                  <span>🔍</span>
                  Analyse
                </div>

                <div
                  class="markdown-body"
                  v-html="renderMarkdown(message.analysis)"
                ></div>

              </div>

            </section>


            <!-- ================= 4. INCIDENT ================= -->

            <section
              v-if="message.incident"
              class="response-card incident-card"
            >

              <div class="section-title">
                <span>🚨</span>
                Incident
              </div>

              <div
                class="markdown-body"
                v-html="renderMarkdown(message.incident)"
              ></div>

            </section>


            <!-- ================= 5. DIAGNOSTIC (causes + actions fusionnées) ================= -->

            <section
              v-if="(message.causes && message.causes.length) || (message.actions && message.actions.length)"
              class="response-card diagnostic-card"
            >

              <div class="diagnostic-grid">

                <div
                  v-if="message.causes && message.causes.length"
                  class="diagnostic-col"
                >

                  <div class="section-title">
                    <span>🔎</span>
                    Causes possibles
                  </div>

                  <ul class="cause-list">

                    <li
                      v-for="(cause, causeIndex) in message.causes"
                      :key="causeIndex"
                    >
                      {{ cause }}
                    </li>

                  </ul>

                </div>

                <div
                  v-if="message.actions && message.actions.length"
                  class="diagnostic-col diagnostic-col-actions"
                >

                  <div class="section-title">
                    <span>🛠️</span>
                    Actions recommandées
                  </div>

                  <ol class="action-list">

                    <li
                      v-for="(action, actionIndex) in message.actions"
                      :key="actionIndex"
                    >
                      {{ action }}
                    </li>

                  </ol>

                </div>

              </div>

            </section>


            <!-- ================= 6. SOURCES (repliables) ================= -->

            <details
              v-if="message.sources && message.sources.length"
              class="response-card sources-card"
            >

              <summary class="section-title sources-summary">
                <span>📚</span>
                Sources utilisées ({{ message.sources.length }})
              </summary>

              <div class="sources">

                <div
                  v-for="(source, sourceIndex) in message.sources"
                  :key="sourceIndex"
                  class="source"
                >

                  <span class="source-number">
                    {{ sourceIndex + 1 }}
                  </span>

                  <span>
                    {{
                      typeof source === 'string'
                        ? source
                        : source.title || source.name || JSON.stringify(source)
                    }}
                  </span>

                </div>

              </div>

            </details>


          </div>

        </div>


        <!-- ================= LOADING ================= -->

        <div
          v-if="loading"
          class="message assistant"
        >

          <div class="avatar">
            🤖
          </div>

          <div class="assistant-content">

            <div class="assistant-header">

              <div class="message-role">
                LogAI
              </div>

            </div>

            <div class="response-card loading-card">

              <div class="loading">

                <div class="loading-dots">
                  <span></span>
                  <span></span>
                  <span></span>
                </div>

                <span>
                  Analyse des logs en cours...
                </span>

              </div>

            </div>

          </div>

        </div>

        <div ref="messagesEndRef"></div>

      </div>


      <!-- ================= ERROR ================= -->

      <div
        v-if="error"
        class="error"
      >
        ⚠️ {{ error }}
      </div>

    </main>


    <!-- =====================================================
         INPUT (zone réorganisée)
    ====================================================== -->

    <footer class="input-area">

      <div class="input-wrapper">

        <form
          class="input-form"
          @submit.prevent="sendMessage"
        >

          <div class="textarea-wrap">

            <textarea
              ref="textareaRef"
              v-model="question"
              rows="1"
              :maxlength="MAX_LENGTH"
              placeholder="Posez votre question sur vos logs... (Entrée pour envoyer, Maj+Entrée pour une nouvelle ligne)"
              :disabled="loading"
              @input="autoResize"
              @keydown="handleKeydown"
            ></textarea>

            <button
              v-if="question.length"
              type="button"
              class="clear-btn"
              title="Effacer"
              @click="clearInput"
            >
              ✕
            </button>

          </div>

          <button
            type="submit"
            class="send-btn"
            :disabled="loading || !question.trim()"
          >

            <span v-if="!loading">
              Envoyer ➤
            </span>

            <span v-else>
              Analyse...
            </span>

          </button>

        </form>

        <div class="input-toolbar">
          <span class="hint">Entrée = envoyer · Maj+Entrée = nouvelle ligne</span>
          <span class="char-count" :class="{ near: charCount > MAX_LENGTH * 0.9 }">
            {{ charCount }}/{{ MAX_LENGTH }}
          </span>
        </div>

      </div>

      <p class="footer-info">
        LogAI • RAG Assistant • Analyse des logs réseau
      </p>

    </footer>

  </div>

</template>


<style>

/* =========================================================
   RESET
========================================================= */

* {
  box-sizing: border-box;
}

html,
body,
#app {
  margin: 0;
  padding: 0;
  width: 100vw;
  min-height: 100vh;
}

body {
  font-family:
    Inter,
    Arial,
    Helvetica,
    sans-serif;

  background: #f5f7fb;
  color: #1f2937;
}


/* =========================================================
   APP
========================================================= */

.app {
  width: 100vw;
  min-height: 100vh;

  display: flex;
  flex-direction: column;
  align-items: stretch;

  background: #f5f7fb;
}


/* =========================================================
   HEADER
========================================================= */

.header {
  width: 100%;

  background: white;

  border-bottom: 1px solid #e5e7eb;

  padding: 18px 40px;
}

.header-content {
  width: 100%;
  max-width: 1100px;

  margin: 0 auto;

  display: flex;
  align-items: center;

  gap: 14px;
}

.logo {
  width: 45px;
  height: 45px;

  display: flex;
  align-items: center;
  justify-content: center;

  border-radius: 12px;

  background: #2563eb;

  font-size: 24px;
}

.header h1 {
  margin: 0;

  font-size: 22px;
  font-weight: 700;
}

.header p {
  margin: 4px 0 0;

  color: #6b7280;

  font-size: 14px;
}


/* =========================================================
   STATUS
========================================================= */

.status {
  margin-left: auto;

  display: flex;
  align-items: center;

  gap: 7px;

  font-size: 12px;

  color: #16a34a;
}

.status-dot {
  width: 8px;
  height: 8px;

  border-radius: 50%;

  background: #22c55e;
}


/* =========================================================
   CHAT
========================================================= */

.chat-container {
  flex: 1;

  width: 100%;
  max-width: 1100px;

  margin: 0 auto;

  padding: 40px 20px 200px;
}


/* =========================================================
   GREETING
========================================================= */

.greeting-card {
  font-size: 15px;
}


/* =========================================================
   EXAMPLES
========================================================= */

.examples {
  display: flex;

  flex-wrap: wrap;

  gap: 10px;

  margin-top: 4px;
}

.examples button {
  display: flex;
  align-items: center;
  gap: 8px;

  padding: 11px 15px;

  background: white;

  border: 1px solid #d1d5db;

  border-radius: 9px;

  cursor: pointer;

  color: #374151;

  font-size: 13.5px;

  transition: 0.2s;
}

.examples button:hover {
  background: #eff6ff;

  border-color: #93c5fd;

  color: #1d4ed8;
}


/* =========================================================
   MESSAGES
========================================================= */

.messages {
  display: flex;

  flex-direction: column;

  gap: 28px;

  margin-top: 28px;
}

.message {
  display: flex;

  gap: 12px;

  align-items: flex-start;
}

.message.user {
  flex-direction: row-reverse;
}

.avatar {
  width: 40px;
  height: 40px;

  min-width: 40px;

  display: flex;

  align-items: center;
  justify-content: center;

  border-radius: 50%;

  background: #e5e7eb;

  font-size: 18px;
}


/* =========================================================
   USER MESSAGE
========================================================= */

.user-content {
  max-width: 75%;

  padding: 13px 17px;

  border-radius: 14px;

  background: #2563eb;

  color: white;

  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.08);
}

.message-role {
  margin-bottom: 6px;

  font-size: 12px;

  font-weight: 600;

  opacity: 0.7;
}

.message-text {
  line-height: 1.6;

  white-space: pre-wrap;

  word-break: break-word;
}


/* =========================================================
   ASSISTANT
========================================================= */

.assistant-content {
  width: min(850px, 90%);

  display: flex;

  flex-direction: column;

  gap: 10px;
}

.assistant-header {
  display: flex;

  align-items: center;

  justify-content: space-between;

  padding: 0 4px;
}

/* Regroupe confiance + sévérité côte à côte dans le header */
.status-badges {
  display: flex;

  align-items: center;

  gap: 8px;
}

.confidence {
  padding: 4px 9px;

  border-radius: 20px;

  background: #ecfdf5;

  color: #047857;

  font-size: 11px;

  font-weight: 600;
}


/* =========================================================
   RESPONSE CARDS
========================================================= */

.response-card {
  background: white;

  border: 1px solid #e5e7eb;

  border-radius: 13px;

  padding: 17px 19px;

  box-shadow:
    0 2px 5px rgba(0, 0, 0, 0.03);
}

.main-response {
  border-left: 4px solid #2563eb;
}

.section-title {
  display: flex;

  align-items: center;

  gap: 8px;

  margin-bottom: 11px;

  font-size: 14px;

  font-weight: 700;

  color: #111827;
}

.response-text {
  line-height: 1.7;

  white-space: pre-wrap;

  word-break: break-word;

  color: #374151;
}

.response-card p {
  margin: 0;

  line-height: 1.7;

  color: #4b5563;
}


/* =========================================================
   SOUS-BLOCS (signification + analyse dans la même carte)
========================================================= */

.sub-block-divider {
  margin-top: 16px;

  padding-top: 16px;

  border-top: 1px dashed #e5e7eb;
}


/* =========================================================
   TEMPLATE
========================================================= */

.template-box {
  padding: 13px;

  border-radius: 8px;

  background: #111827;

  color: #e5e7eb;

  font-family:
    Consolas,
    Monaco,
    monospace;

  font-size: 13px;

  line-height: 1.6;

  word-break: break-word;
}


/* =========================================================
   INCIDENT
========================================================= */

.incident-card {
  border-left: 4px solid #b91c1c;
}


/* =========================================================
   CAUSES
========================================================= */

.cause-list {
  margin: 0;

  padding-left: 22px;

  color: #4b5563;
}

.cause-list li {
  margin-bottom: 8px;

  line-height: 1.5;
}


/* =========================================================
   DIAGNOSTIC (causes + actions regroupées)
========================================================= */

.diagnostic-card {
  border-left: 4px solid #16a34a;
}

.diagnostic-grid {
  display: grid;

  grid-template-columns: 1fr 1fr;

  gap: 22px;
}

.diagnostic-col-actions {
  padding-left: 22px;

  border-left: 1px solid #e5e7eb;
}

.action-list {
  margin: 0;

  padding-left: 22px;

  color: #374151;
}

.action-list li {
  margin-bottom: 10px;

  padding-left: 5px;

  line-height: 1.5;
}


/* =========================================================
   SOURCES
========================================================= */

.sources-card {
  background: #f9fafb;
}

.sources-summary {
  cursor: pointer;

  margin-bottom: 0;

  list-style: none;
}

.sources-summary::-webkit-details-marker {
  display: none;
}

.sources-card[open] .sources-summary {
  margin-bottom: 11px;
}

.sources {
  display: flex;

  flex-direction: column;

  gap: 8px;
}

.source {
  display: flex;

  align-items: flex-start;

  gap: 9px;

  font-size: 13px;

  color: #4b5563;

  line-height: 1.5;
}

.source-number {
  width: 22px;
  height: 22px;

  min-width: 22px;

  display: flex;

  align-items: center;
  justify-content: center;

  border-radius: 50%;

  background: #dbeafe;

  color: #1d4ed8;

  font-size: 11px;

  font-weight: 700;
}


/* =========================================================
   SEVERITY
========================================================= */

.severity {
  padding: 4px 10px;

  border-radius: 20px;

  font-size: 11px;

  text-transform: uppercase;

  font-weight: 600;
}

.severity.info {
  background: #dbeafe;

  color: #1d4ed8;
}

.severity.warning {
  background: #fef3c7;

  color: #92400e;
}

.severity.alert,
.severity.error,
.severity.critical {
  background: #fee2e2;

  color: #b91c1c;
}


/* =========================================================
   LOADING
========================================================= */

.loading-card {
  padding: 15px 18px;
}

.loading {
  display: flex;

  align-items: center;

  gap: 10px;

  color: #6b7280;

  font-size: 14px;
}

.loading-dots {
  display: flex;

  gap: 4px;
}

.loading-dots span {
  width: 6px;
  height: 6px;

  background: #6b7280;

  border-radius: 50%;

  animation: bounce 1.4s infinite;
}

.loading-dots span:nth-child(2) {
  animation-delay: 0.2s;
}

.loading-dots span:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes bounce {

  0%,
  80%,
  100% {
    transform: translateY(0);
  }

  40% {
    transform: translateY(-5px);
  }

}


/* =========================================================
   ERROR
========================================================= */

.error {
  margin-top: 20px;

  padding: 14px 18px;

  background: #fee2e2;

  border: 1px solid #fecaca;

  color: #991b1b;

  border-radius: 10px;
}


/* =========================================================
   INPUT (réorganisé)
========================================================= */

.input-area {
  position: fixed;

  bottom: 0;

  left: 0;
  right: 0;

  background: white;

  border-top: 1px solid #e5e7eb;

  padding: 15px 20px 10px;

  z-index: 10;

  box-shadow: 0 -4px 12px rgba(0, 0, 0, 0.03);
}

.input-wrapper {
  width: 100%;
  max-width: 1100px;

  margin: 0 auto;
}

.input-form {
  display: flex;

  align-items: flex-end;

  gap: 10px;
}

.textarea-wrap {
  position: relative;

  flex: 1;
}

.input-form textarea {
  width: 100%;

  resize: none;

  max-height: 160px;

  padding: 13px 40px 13px 17px;

  border: 1px solid #d1d5db;

  border-radius: 14px;

  font-size: 15px;

  font-family: inherit;

  line-height: 1.5;

  outline: none;
}

.input-form textarea:focus {
  border-color: #2563eb;

  box-shadow:
    0 0 0 2px rgba(37, 99, 235, 0.1);
}

.clear-btn {
  position: absolute;

  top: 10px;
  right: 8px;

  width: 22px;
  height: 22px;

  border: none;

  border-radius: 50%;

  background: #e5e7eb;

  color: #6b7280;

  font-size: 11px;

  cursor: pointer;

  display: flex;
  align-items: center;
  justify-content: center;
}

.clear-btn:hover {
  background: #d1d5db;
}

.send-btn {
  padding: 0 22px;

  height: 46px;

  border: none;

  border-radius: 12px;

  background: #2563eb;

  color: white;

  cursor: pointer;

  font-size: 15px;

  font-weight: 600;

  white-space: nowrap;
}

.send-btn:hover:not(:disabled) {
  background: #1d4ed8;
}

.send-btn:disabled {
  background: #9ca3af;

  cursor: not-allowed;
}

.input-toolbar {
  display: flex;

  justify-content: space-between;

  margin-top: 6px;

  padding: 0 4px;

  font-size: 11px;

  color: #9ca3af;
}

.char-count.near {
  color: #b91c1c;
}


/* =========================================================
   FOOTER
========================================================= */

.footer-info {
  text-align: center;

  margin: 8px 0 0;

  font-size: 11px;

  color: #9ca3af;
}


/* =========================================================
   MOBILE
========================================================= */

@media (max-width: 700px) {

  .header {
    padding: 15px 20px;
  }

  .header-content {
    max-width: none;
  }

  .status {
    display: none;
  }

  .chat-container {
    padding: 25px 12px 210px;
  }

  .user-content {
    max-width: 85%;
  }

  .assistant-content {
    width: 85%;
  }

  .examples {
    flex-direction: column;
  }

  .examples button {
    width: 100%;
  }

  .input-toolbar .hint {
    display: none;
  }

  .diagnostic-grid {
    grid-template-columns: 1fr;

    gap: 16px;
  }

  .diagnostic-col-actions {
    padding-left: 0;

    border-left: none;

    padding-top: 16px;

    border-top: 1px dashed #e5e7eb;
  }

}
</style>