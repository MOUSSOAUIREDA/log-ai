


def generate_markdown_report(result : dict ) -> str : 
    
    markdown = []
    
    markdown.append("# Analyse technique des logs : ")
    markdown.append("")
    
    for vendor , topics in result.items() : 
        
        markdown.append(f"## Vendeur : {vendor}")
        markdown.append("")    
            
        for topic , levels in topics.items() : 
            
            markdown.append(f"### Topic : {topic}")
            markdown.append("")
            
            for level , templates in levels.items() : 
                
                markdown.append(f"#### Level : {level}")
                markdown.append("")
                
                for template in templates : 
                    
                    markdown.append(f"##### Template : {template['template']} ")
                    markdown.append("")
                    
                    markdown.append(f"- **Occurences :** {template['count']}")
                    markdown.append(f"- **First seen :** {template['first_seen']}")
                    markdown.append(f"- **Last seen :** {template['last_seen']}")
                    markdown.append("")
                     
                    markdown.append("- **Examples :** ")     
                    markdown.append("")
                    
                    for example in template['examples'] : 
                        markdown.append(f"- `{example}`")
                        
                    markdown.append("")              
    return "\n".join(markdown)