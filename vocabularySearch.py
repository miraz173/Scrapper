import requests
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
}

def getInfo(query):
    url = f"https://www.google.com/search?client=ubuntu-sn&channel=fs&q={query}+meaning"

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    element = soup.find(class_="vmod")

    if not element:
        print(f"For {query}, Element with class 'vmod' not found.")
        return {"word":query, "partsOfSpeech":'', "Definitions":'', "Example": '', "Similarity":[], "Dissimilarity": []}


    else:
        partsOfSpeech = soup.find(class_="YrbPuc").text if soup.find(class_="YrbPuc") else 'N/A'
        print(f"    {query}: ({partsOfSpeech})")  # or use `print(element)` for the full HTML

        target = soup.find(class_="thODed")
        if not target:
            print(f"Error! {query} not found")
            return {"word":query, "partsOfSpeech":partsOfSpeech, "Definitions":'', "Example": '', "Similarity":[''], "Dissimilarity": ['']}
        else:
            target = target.find_all(class_="wHYlTd sY7ric")

        ans=[]
        defs=[]
        exmpls=[]
        sims=[]
        dissims=[]
        for i in target[1:]:
            obj=[]
            ##
            definition_Example=i.find(class_="PZPZlf")

            definition=definition_Example.find("div", style="display:inline")
            print(f"Definition:    {definition.text}")
            obj.append(definition.text)
            defs.append(definition.text)
            
            example=definition_Example.find(class_="ZYHQ7e")
            if example.text:
                print(f"Example:    {example.text}")
                obj.append(example.text)
                exmpls.append(example.text)
            else:
                print(f"Example: 404 NOT FOUND")
                obj.append('404 not found')
                exmpls.append('404 not found')

            ##

            sim_dissim=i.find(class_="bqVbBf jfFgAc CqMNyc")
            if not sim_dissim:
                print(f"sim dissim of {query} not found")
                return {"word":query, "partsOfSpeech":partsOfSpeech, "Definitions":defs, "Example": exmpls, "Similarity":[''], "Dissimilarity": ['']}

            else:
                sim_dissim=sim_dissim.find_all("div", class_=["mlJB3e LxXWyd", "qFRZdb"])
                for i in sim_dissim:
                    x=i.find(class_=["pdpvld", "hVpeib"])
                    if x and (x.text=="Similar:" or x.text=="একইরকম:"):
                        print("similar Words:  ", end=' ')
                        elmnt=[]
                    elif x and (x.text=="Opposite:" or x.text=="বিপরীত:"):
                        print("\nOpposite Words:  ", end=' ')
                        obj.append(elmnt)
                        sims.append(elmnt)
                        elmnt=[]
                    else:
                        print(i.text, end=", ")
                        elmnt.append(i.text)
                print("\n")
                ans.append(obj)
                dissims.append(elmnt)

        return {"word":query, "partsOfSpeech":partsOfSpeech, "Definitions":defs, "Example": exmpls, "Similarity":sims, "Dissimilarity": dissims}


queries=["frivolous", "feckels", "taciturn", "scrupolous", "aloof", "flippant", "zealous", "austere", "exacting", "vendetta", "meticulous"]
result=[]
for query in queries:
    try:
        result.append(getInfo(query))
    except:
        print("Error at ", query)
    

html = """<!DOCTYPE html>
<html>
    <head>
        <title>Two Sub-Rows in a Row</title>
        <style>
            table {
                border-collapse: collapse;
                width: 100%;
            }
            th, td {
                border: 1px solid black;
                padding: 8px;
                text-align: left;
            }
            .sub-table td {
                border: none;
            }
        </style>
    </head>
    <body>
        <table>
            <thead>
                <tr>
                    <th>Word</th>
                    <th>Part of Speech</th>
                    <th>Definition</th>
                    <th>Example</th>
                    <th>Synonims</th>
                    <th>Antonyms</th>
                </tr>
            </thead>
            <tbody>"""

for i in result:
    for j in range(len(i["Similarity"])):
        if j == 0:
            html += f"""
                <tr>
                    <td rowspan={len(i['Similarity'])}>{i['word']}</td>
                    <td rowspan={len(i['Similarity'])}>{i['partsOfSpeech']}</td>
                    <td>{i['Definitions'][j]}</td>
                    <td>{i['Example'][j]}</td>
                    <td>{", ".join(i['Similarity'][j])}</td>
                    <td>{", ".join(i['Dissimilarity'][j])}</td>
                </tr>"""
        else:
            html += f"""
                <tr>
                    <td>{i['Definitions'][j]}</td>
                    <td>{i['Example'][j]}</td>
                    <td>{", ".join(i['Similarity'][j])}</td>
                    <td>{", ".join(i['Dissimilarity'][j])}</td>
                </tr>"""

html += """
            </tbody>
        </table>
    </body>
</html>"""

# Save the output
with open("output.html", "w") as f:
    f.write(html)

