#!ruby
#!/usr/bin/ruby
require 'net/http'
Net::HTTP.start("txt.bookdown.net") { |http|
r = http.get("/home/down/txt/id/625")
open("625.txt", "wb") { |file|
file.write(r.body)
}
}