package main

import (
        ."fmt"
        "html/template"
        "io"
        "net/http"
        "os"
)

func index(w http.ResponseWriter, r *http.Request) {
        const upload = `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>后台管理</title>
  <link rel="stylesheet" href="https://cdn.staticfile.org/twitter-bootstrap/3.3.7/css/bootstrap.min.css" >
</head>
<body>
<form method="post" enctype="multipart/form-data">
  <input type="file" name="file">
  <input type="submit">
</form>
<a href="/img/{{.URL}}">{{.URL}}</a>
</body>
</html>`
        t := template.Must(template.New("upload").Parse(upload))
        file, handle, err := r.FormFile("file")
        if err == nil {
                Println(handle.Filename)
                type recipient struct {
                        URL string
                }
                var recipients = recipient{handle.Filename}
				//需要在 a.go 同级目录提前创建img文件夹，不会自动创建
				//漏洞触发点
                f, _ := os.OpenFile("img/"+handle.Filename, os.O_WRONLY|os.O_CREATE, 0666)
                io.Copy(f, file)
                defer f.Close()
                t.Execute(w, recipients)
        } else {
                t.Execute(w, nil)

        }

}

func main() {
        http.HandleFunc("/index.php", index)
        http.HandleFunc("/", index)
        http.Handle("/img/", http.StripPrefix("/img", http.FileServer(http.Dir("./img"))))
        http.ListenAndServe("0.0.0.0:8080", nil)}
