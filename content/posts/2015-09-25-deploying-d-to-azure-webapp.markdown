---
author: Jeremy
comments: true
date: 2015-09-25 20:10:00+07:00
layout: post
slug: deploying-d-to-azure-webapp
title: 4 Simple Steps to Run D Language in Azure Websites
categories:
- D
Tags:
- Azure
---

_I shameless stole these steps from [4 Simple Steps to Run Go Language in Azure Websites](http://www.wadewegner.com/2014/12/4-simple-steps-to-run-go-language-in-azure-websites/). This post is simply a transliteration to D. Thank you very much to Wade Wegner for the original post._

# 4 Simple Steps

1. Create your Azure Website in Azure Portal. 
	1. Configure FTP deployment

![FTP Configuration](/img/Azure-FTP-Config.png)

2&#46; Run ```dub init vibed_hello_world --type=vibe.d``` and change the default app.d to read the port from an environment variable. [Docs](https://vibed.org/docs)
```d
import vibe.d;

shared static this()
{
	import std.process;
	import std.conv;

	immutable port = environment["HTTP_PLATFORM_PORT"]; //Use the port IIS tells us to.

	auto settings = new HTTPServerSettings;
	settings.port = to!ushort(port);
	settings.bindAddresses = ["::1", "127.0.0.1"];
	listenHTTP(settings, &hello);

	logInfo("Please open http://127.0.0.1:" ~ port ~ "/ in your browser.");
}

void hello(HTTPServerRequest req, HTTPServerResponse res)
{
	res.writeBody("Hello, World!");
}
```

3&#46; Create Web.Config

```xml
<?xml version="1.0" encoding="UTF-8"?>
<configuration>
	<system.webServer>
		<handlers>
			<add name="httpplatformhandler" path="*" verb="*" modules="httpPlatformHandler" resourceType="Unspecified" />
		</handlers>
		<httpPlatform processPath="d:\home\site\wwwroot\vibed_hello_world.exe" 
					arguments="" 
					startupTimeLimit="60">
			<environmentVariables>
			</environmentVariables>
		</httpPlatform>
	</system.webServer>
</configuration>
```
4&#46; Upload binaries and DLLs to Azure! 
![Upload to FTP Server](/img/upload-to-ftp.png)
