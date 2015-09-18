topics = ("rfc snmp information data type management snmpv page protocol description model object ipfix configuration set transport standards defined track field",
"protocol host internet rfc network telnet user page standard postel information system mail protocols hosts ftp tcp nic file computer",
"description status mib current syntax object object-type rfc max-access objects read-only table management page integer counter track standards group access",
"network service information informational internet system security services requirements protocols data provide networks accepted management systems application protocol architecture access",
"context adsl sha page rfc int gss-api iscsi dsx data bits return integer scsi input bit api code interval line",
"router link state ospf routing type interface rfc network routers neighbor packet area set section address page packets protocol tlv",
"rfc rtp payload packet header media format session type track standards source page packets section stream data bit number field",
"rfc message mail header character text http field page characters mime section smtp defined user format information type fields body",
"ipv address rfc node mobile addresses option network home agenthost nat dns packet page mobility port section source packets",
"server client command file response nfs data servers request rfc page operation clients protocol list section set track standards system",
"rfc document internet ietf standards rights protocol considerations references copyright page iana security information documents bcp informational society email track",
"key certificate rfc algorithm signature page public identifier encryption sequence security object certificates message keys section type autheneld",
"server authentication rfc client authorization access security peer tls protocol user section session request eap page radius identity attribute service",
"message messages data protocol request field state error length type connection response number received control page address send code section",
"sip rfc request call media header session proxy page invite user event conference response tag uri field alice bob gateway",
"rfc label path mpls traffic lsp node signaling rsvp qos document page object link control lsr set section ldp network",
"packet tcp packets data time flow number rfc rate congestion control connection page segment delay sequence measurement size loss option",
"attribute element rfc type xml object attributes page section document printer track uri information location standards namespace elements resource values",
"author doc-id rfc title format stream date doi year file-format char-count month current-status publication-status rfc-entry page-count abstract keywords draft wg_acronym",
"address multicast route routing rfc bgp vpn group router source addresses page information atm routes network set packet protocol routers",)



i = 0;
for topic in topics:
	print('<div class="topic,topic{0}">'.format(i))
	print('<span class="title">{}</span>')
	print('<div class="terms">')
	print "<ul>"
	for word in topic.split():
		print("<li>{0}</li>".format(word))
	print "</ul>"
	print "</div>"
	print "</div>"
	i = i + 1

