<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<%@ page import="org.apache.catalina.core.StandardContext" %>
<%@ page import="org.apache.catalina.core.StandardEngine" %>
<%@ page import="org.apache.catalina.core.StandardHost" %>
<%@ page import="java.lang.reflect.Field" %>
<%@ page import="java.util.HashMap" %>
<%@ page import="java.util.Iterator" %>
<%@ page import="java.util.logging.Logger" %>


<%!
    String uri;
    String serverName;
    StandardContext standardContext;

    public Object getField(Object object, String fieldName) {
        Logger log3 = Logger.getLogger("113");
        Field declaredField;
        Class clazz = object.getClass();
        while (clazz != Object.class) {
            try {
                declaredField = clazz.getDeclaredField(fieldName);   // 取得这个类自己定义的所有公开的私有的字段,但是不包括继承的字段
                declaredField.setAccessible(true);
                return declaredField.get(object);
            } catch (NoSuchFieldException e) {
                //log3.info(e.toString()); //java.lang.NoSuchFieldException
            } catch (IllegalAccessException e) {
                log3.info(e.toString());
            }
            clazz = clazz.getSuperclass();
        }
        return null;
    }


    public void getStandardContext() {
        String ANSI_YELLOW = "\u001B[33m";
        String ANSI_GREEN = "\u001B[32m";
        String ANSI_RESET = "\u001B[0m";
        Logger log2 = Logger.getLogger("113");
        log2.info(ANSI_YELLOW + "getStandardContext method ing..." + ANSI_RESET);
        Thread[] threads = (Thread[]) this.getField(Thread.currentThread().getThreadGroup(), "threads");
        //log2.info(String.valueOf(threads.length));  //32

        for (Thread thread : threads) {
            // 过滤掉不相关的线程
            if (thread == null || thread.getName().contains("exec")) {
                continue;
            }

            if ((thread.getName().contains("Acceptor") || thread.getName().contains("Poller")) && (thread.getName().contains("http"))) {  // thread  http-nio-8080-Acceptor
                log2.info("thread: " + thread.getName());
                Object target = this.getField(thread, "target"); //target org.apache.tomcat.util.net.Acceptor@6698f6ae
                log2.info("target: " + target.toString());
                HashMap children;
                Object jioEndPoint = null;

                // Poller 线程
                if (thread.getName().contains("Poller")) {
                    try {
                        jioEndPoint = getField(target, "this$0");  //等价于  thread.getClass().getDeclaredField("this$0");  // Poller 线程
                        log2.info("jioEndPoint: " + jioEndPoint.toString());
                    } catch (Exception e) {
                        //log2.info(e.toString());  //java.lang.NullPointerException
                    }
                } else
                    // Acceptor 线程
                    if (thread.getName().contains("Acceptor")) {
                        //if (jioEndPoint == null) {
                        try {
                            jioEndPoint = getField(target, "endpoint");  // org.apache.tomcat.util.net.NioEndpoint@4eaaa9
                            log2.info("jioEndPoint: " + jioEndPoint.toString());
                        } catch (Exception e) {
                            log2.warning("异常，准备return " + e.toString());
                            return;
                        }
                    }
                Object service = getField(getField(getField(getField(getField(jioEndPoint, "handler"), "proto"), "adapter"), "connector"), "service");
                log2.info("service: " + service.toString());   // StandardService[Catalina]
                StandardEngine engine = null;
                try {
                    // tomcat 6,7,8
                    engine = (StandardEngine) getField(service, "container");
                    log2.info("engine: " + engine.toString());
                } catch (Exception e) {
                    //log2.info(e.toString());  //java.lang.NullPointerException
                }
                if (engine == null) {
                    // tomcat 9
                    engine = (StandardEngine) getField(service, "engine");  // StandardEngine[Catalina]
                    log2.info("engine: " + engine.toString());
                }

                children = (HashMap) getField(engine, "children");  //{localhost=StandardEngine[Catalina].StandardHost[localhost]}
                log2.info("children: " + children.toString());
                try {
                    // 这里使用ip会有问题会走catch的逻辑，也可以都用catch的逻辑代替
                    StandardHost standardHost = (StandardHost) children.get(this.serverName);
                    children = (HashMap) getField(standardHost, "children");
                    log2.info("standardHost: " + standardHost.toString());
                    Iterator iterator = children.keySet().iterator();
                    while (iterator.hasNext()) {
                        String contextKey = (String) iterator.next();
                        if (!(this.uri.startsWith(contextKey))) {
                            continue;
                        }
                        StandardContext standardContext = (StandardContext) children.get(contextKey);
                        this.standardContext = standardContext;
                        return;
                    }
                } catch (Exception e) {
                    // 不管是用 ip 还是 localhost 访问 最终都是走这个逻辑   children.get("localhost");
                    //log2.info(e.toString());  // java.lang.NullPointerException

                    StandardHost standardHost = (StandardHost) children.get("localhost");
                    log2.info("standardHost: " + standardHost.toString());
                    try {
                        children = (HashMap) getField(standardHost, "children");
                        Iterator iterator = children.keySet().iterator();
                        while (iterator.hasNext()) {
                            String contextKey = (String) iterator.next();
                            if (this.uri.startsWith(contextKey) && contextKey != "") {
                                StandardContext standardContext = (StandardContext) children.get(contextKey);
                                this.standardContext = standardContext; // StandardEngine[Catalina].StandardHost[localhost].StandardContext[/untitled3_war_exploded]
                                log2.warning(ANSI_GREEN + "standardContext: " + standardContext.toString() + ANSI_RESET);
                                return;
                            }
                        }
                    } catch (Exception e2) {
                        //log2.info(e2.toString()); //java.lang.NoSuchFieldException: children
                    }
                }
            }
        }
    }

    public StandardContext getSTC() {
        return this.standardContext;
    }

%>
<%
    String ANSI_RESET = "\u001B[0m";
    String ANSI_RED = "\u001B[31m";
    String ANSI_GREEN = "\u001B[32m";
    String ANSI_YELLOW = "\u001B[33m";
    Logger log = Logger.getLogger("main");

    Thread[] threads = (Thread[]) this.getField(Thread.currentThread().getThreadGroup(), "threads"); // tomcat 线程
    Object object;
    for (Thread thread : threads) {
        if (thread == null || thread.getName().contains("exec")) {
            continue;
        }
        log.info(ANSI_RED + "main_thread: " + thread + ANSI_RESET);        // 打印 线程  // Thread[main,5,main]  // Thread[Monitor Ctrl-Break,5,main]
        if (thread.getName().contains("Acceptor") || thread.getName().contains("Poller")) {
            Object target = this.getField(thread, "target");  //! target instanceof Runnable
            log.info("main_target: " + target);
            log.info(String.valueOf(target instanceof Runnable));
            if (!(target instanceof Runnable)) {
                continue;
            }

            try {
                object = getField(getField(getField(target, "this$0"), "handler"), "global");
            } catch (Exception e) {
                //log.warning(ANSI_RED+e.toString()+ANSI_RESET); // java.lang.NoSuchFieldException
                continue;
            }
            if (object == null) {
                continue;
            }
            java.util.ArrayList processors = (java.util.ArrayList) getField(object, "processors");
            Iterator iterator = processors.iterator();
            while (iterator.hasNext()) {
                Object next = iterator.next();
                Object req = getField(next, "req");   // 获取 req 对象
                // 过滤 // req: R( null)
                Object serverPort = getField(req, "serverPort");
                if (serverPort.equals(-1)) {   // 不是对应的请求时，serverPort = -1
                    continue;
                }
                log.info("req: " + req.toString());  // req: R( /untitled3_war_exploded/2.jsp)

                org.apache.tomcat.util.buf.MessageBytes serverNameMB = (org.apache.tomcat.util.buf.MessageBytes) getField(req, "serverNameMB");
                this.serverName = (String) getField(serverNameMB, "strValue");
                if (this.serverName == null) {
                    this.serverName = serverNameMB.toString();
                }
                if (this.serverName == null) {
                    this.serverName = serverNameMB.getString();
                }
                log.info(this.serverName.toString());  // 10.10.40.65
                org.apache.tomcat.util.buf.MessageBytes uriMB = (org.apache.tomcat.util.buf.MessageBytes) getField(req, "uriMB");
                this.uri = (String) getField(uriMB, "strValue");
                if (this.uri == null) {
                    this.uri = uriMB.toString();
                }
                if (this.uri == null) {
                    this.uri = uriMB.getString();
                }
                log.info(this.uri.toString());

                this.getStandardContext();

                //return;


            }
        }


    }
%>