import os
import json

def extract_data_from_xml(xml_file):
    try:
        
        with open(xml_file, 'r', encoding='iso-8859-1', errors='replace') as f:
            content = f.read()
        
        #Extract HEADLINE
        headline_start = content.find('<HEADLINE ID="2:105">') + len('<HEADLINE ID="2:105">')
        headline_end = content.find('</HEADLINE>', headline_start)
        headline = content[headline_start:headline_end].strip() if headline_start != -1 and headline_end != -1 else ""
        
        #Extract BRODTEXT
        brodtext_start = content.find('<BRODTEXT>') + len('<BRODTEXT>')
        brodtext_end = content.find('</BRODTEXT>', brodtext_start)
        brodtext_content = content[brodtext_start:brodtext_end] if brodtext_start != -1 and brodtext_end != -1 else ""
        
        #Extract all <P> tags from BRODTEXT
        body_text = []
        p_start = brodtext_content.find('<P>')
        while p_start != -1:
            p_end = brodtext_content.find('</P>', p_start)
            if p_end != -1:
                p_text = brodtext_content[p_start+3:p_end].strip()
                if p_text:
                    body_text.append(p_text)
                p_start = brodtext_content.find('<P>', p_end)
            else:
                break
        body = " ".join(body_text)
        
        return headline, body
    
    except Exception as e:
        print(f"Error processing {xml_file}: {str(e)}")
        return None, None

def process_directory_to_jsonl(root_dir, output_file):
    with open(output_file, 'w', encoding='utf-8') as jsonl_file:
        for dirpath, _, filenames in os.walk(root_dir):
            for filename in filenames:
                if filename.lower().endswith('.xml'):
                    xml_file = os.path.join(dirpath, filename)
                    headline, body = extract_data_from_xml(xml_file)
                    
                    if headline and body:

                        messages = [
                            {"role": "system", "content": "Du är en assistent som hjälper till att skapa rubriker för nyhetsartiklar."},
                            {"role": "user", "content": f"Skapa en rubrik för denna artikel:\n\n{body}"},
                            {"role": "assistant", "content": headline}
                        ]
                        
                        json_obj = {"messages": messages}
                        jsonl_file.write(json.dumps(json_obj, ensure_ascii=False) + '\n')


input_dir = 'clefkorpus'
output_jsonl = 'headline'
process_directory_to_jsonl(input_dir,output_jsonl)