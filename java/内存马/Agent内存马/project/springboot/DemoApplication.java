package com.example.demo;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseBody;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.ObjectInputStream;

@SpringBootApplication
@Controller
public class DemoApplication {

    public static void main(String[] args) {
        SpringApplication.run(DemoApplication.class, args);
    }

    @ResponseBody
    @RequestMapping("/cc5")
    public String cc5Vuln(HttpServletRequest request, HttpServletResponse response) throws Exception {
        java.io.InputStream inputStream = request.getInputStream();
        ObjectInputStream objectInputStream = new ObjectInputStream(inputStream);
        try {
            String a = objectInputStream.readObject().toString();
            System.out.println(a);
        } catch (Exception e) {
            System.out.println(e);
        }
        return "Hello,World";
    }

    @ResponseBody
    @RequestMapping("/demo")
    public String demo(HttpServletRequest request, HttpServletResponse response) throws Exception {
        return "This is OK Demo!";
    }

    @ResponseBody
    @RequestMapping("/Filter2")
    public void demo2(HttpServletRequest request, HttpServletResponse response) throws Exception {
    }
}
