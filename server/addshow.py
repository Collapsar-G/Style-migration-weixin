import json

if __name__ == "__main__":
    # temp = {}
    f = open('./static/json/show.json', 'r', encoding="UTF-8")
    content = f.read()
    f.close()

    print(content)
    temp = json.loads(content)

    temp["num"] += 1
    url = ["https://cdn.jsdelivr.net/gh/Collapsar-G/image/img/20210207111449.png",
           "https://cdn.jsdelivr.net/gh/Collapsar-G/image/img/20210206154613.jpg"]
    # temp["images"] ={}
    temp["images"][temp["num"]] = url
    print(temp)

    js = json.dumps(temp)
    f = open('./static/json/show.json', 'w', encoding="UTF-8")
    f.write(js)
    f.close()
