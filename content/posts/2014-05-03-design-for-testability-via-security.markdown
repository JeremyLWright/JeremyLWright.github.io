---
author: admin
comments: true
date: 2014-05-03 20:56:49+00:00
layout: post
slug: design-for-testability-via-security
title: 'Design for Testability via Security '
wordpress_id: 603
categories:
- Security
tags:
- '747'
- bootloader
- firmware
- hash
- Security
- test
- verify
---

I was discussing bootloader design with a colleague of mine the other day. We were attempting to load new a third-party hardware component. The device has a poor protocol, and a useless verification step. This discussion got me thinking however how the concepts used to build a strong self-enforcing security protocol, also apply to building a testable, and reliable communication protocol. Thus, security helps us build better products not because they are secure, but because they are verifiable. 
<!-- more -->
This idea initially struck me as strange, since many of the secure software interfaces I've used in the past, are quite obtuse. This is not a fundamental aspect of security, by rather an artifact of poor design (think OpenSSL). This is sad, since security is already a difficult concept, and requires a great deal of study to maintain throughout the life cycle of a product. Secure interfaces should make security easier, not more difficult. This is however a separate rant. So back to the bootloader.

This specific device is connected by a CAN bus. This is not critical to my argument except the fact that CAN is a reliable, but slow and message order is not guaranteed. In fact, within a window of 4 packets, order is essentially random. Think about this for a moment: load firmware with random message order. The goal is to design a protocol to work with this. Firmware loading fits into a three step process: Prepare, Load, Verify. This process works independent of underlying storage techniques. For example, NAND must be erased on a full page boundary, that can be done in the prepare step. Loading to a file system, Prepare might be a simple NOP.

Firstly, know that the final, verification step is essential. Some environments, the bootloader runs out of RAM, if the load process fails, and the hardware reboots without verification, the bootloader may no longer function, and you just build a sweet digital brick. So verification must check that the firmware the user attempted to load, matches the firmware written to the flash. There are several mechanisms to verify this. The hardware my colleague and I are working with, simply reads the flash back to you. At a high level this sounds fine.


    
    Loader ---> Send Data     ---> Bootloader
    Loader ---> Data Complete ---> Bootloader
    Loader ---> Verify        ---> Bootloader
    Loader <--- Send Data     <--- Bootloader
    Loader Loader Verifies data matches.
    



Remember, message order is random. If the bootloader dumps its flash back on the CAN bus, without a sequence number or flash addresses, the data that comes back is completely useless. Each data packet is intact, but is position within the overall data block is unknown. The best one can do is probabilisticly reorder the packets to attempt to get a confidence the bootloader has the same data we attempted to send. Okay, so what would be better? Lets model this as a security problem and design a secure document sending protocol.



### Prepare


Alice and Bob want to exchange a document. (Any protocol can be made more "secure" by describing it with [Alice and Bob.](https://xkcd.com/1323/)) The communication channel is UDP, untrusted, and public. How should Alice and Bob communicate? Every security protocol starts with authentication. Bob wants to verify the sender is Alice. Alice wants to verify it's sending the document to Bob, and not someone else. So lets negotiate a key based on a preshared secret. This will form the prepare step of our high-level bootloader model.
<table >
<tr >

<td >Alice generates a nonce.
</td>

<td >
</td>

<td >Bob waiting for message.
</td>
</tr>
<tr >

<td >Alice encrypts bob_public_key(nonce_alice:sha256(nonce_alice))
</td>

<td >->
</td>

<td >Bob
</td>
</tr>
<tr >

<td >Alice
</td>

<td ><-
</td>

<td >Bob decrypts the message.
Bob generates a new nonce. Bob encrypts 
alice_public_key(nonce_bob:sha256(nonce_bob):nonce_alice:sha256(nonce_alice))

</td>
</tr>
</table>

Alice now has Bob's nonce. Bob has Alice's nonce. Any listening attacker only has 2 messages of cipher text. Bob know's the message was sent from Alice because only Alice has Alice's private key,thus only Alice could have made the nonce message. Bob knows the nonce was intentional because Alice included the secure hash of the nonce. 

This protocol is protected against replay attack since Bob decrypts the nonce and hash, and reencrypts with Alice's public key. This allows Alice to verify Bob received her original message. Furthermore the messages are protected against manipulation because all messages include hashes. Bob, and Alice are authenticated. Additionally, they share a new, secret session key.

Alice builds the session key, "sha256(nonce_bob:nonce_alice)".

Bob builds the session key, "sha256(nonce_bob:nonce_alice)".  

Now only Bob and Alice at this time instance can have this new shared secret. Alice and Bob can now communicate securely. <del>Let's load some firmware to Bob now.</del> Let's transfer a document to Bob now.



### Transfer


Alice creates a document and signs it e.g. document:alice_private_key(sha256(document)).  Notice that Alice's private key is used to encrypt here. This is correct. We want Bob to receive the document, create a hash of the document. Bob then uses Alice's public key to "encrypt" the signature sent by Alice. He will get the plain text hash, and compare. The signature does not protect the hash i.e. it does not provide confidentiality since anyone can decrypt with the public key. Instead the signature provides integrity. The hash protects that the document was unchanged. The signature of the hash protects that the hash was computed only by Alice. 

Alice breaks up the document into packets to send over UDP. Each packet includes a sequence number and a hash of that message.

packet = aes(session_key, i:document[i]:sha256(i:document[i]))

The session key encrypts the entire message to provide confidentiality. This also strengthens the Man in the middle attack, since this session_key is ephemeral. Since it exists for only this authenticated session, an attacker cannot resend this data later to Bob. The sha256 hash provides integrity i.e. <del>transmission errors</del> malicious corruption. Bob verifies each individual packet by calculating the has of the received document[i], and comparing it. If the packets arrive out of order, which in <del>CAN</del> UDP they will, Bob can sort them. 

Once Bob has the entire message he can verify the signature.  Bob now has the document, all listeners only have cipher version of the document. Furthermore, Bob can verify the entire document is valid. Bob will <del>erase his flash, and load the new firmware into memory</del> PROFIT! 



### Verify


The device my colleague and I are trying to fix simply dumped the document back to Alice.  Essentially:

packet = document[i]

Each packet isn't protected from corruption. The order of the document is unverifiable. The best Alice can do is attempt to verify multiple times hoping the document messages randomly converge on the document Alice originally sent. This is the same as using [Bogosort](http://en.wikipedia.org/wiki/Bogosort) as a verification step. Not awesome. Instead we've built up some very secure machinery to <del>load software reliably</del> transfer a document securely. 

One method, although rather naive would be for Bob to send back the document to Alice in the same manner, encrypting each packet and the final signature. This however is very wasteful. Instead Alice only needs to confirm that Bob has the document in its entirely, that it is in the flash, and that all packets were loaded in the correct order. Bob simply needs to send a signature. Bob then reads his flash, and calculates a sha256. Bob then sends 1 message:

packet = aes(session_key, bob_private_key(sha256(flash_read)))

The packet is confidential because it is encrypted by aes. The message is protected from integrity because Alice already has the hash, she simple needs to verify that it matches the know value. Note that if Alice didn't have the hash already we would include a hash of the hash to provide further integrity. Alice knows that it was Bob who verified the flash because the hash is signed with Bob's key. Lastly, Alice knows the message is part of this load session and not a previous one replayed by an attacker because the whole message is encrypted by a session key. 



### Conclusion


Alice and Bob now have a protocol secure against a number of attacks, but how is this useful for a bootloader? Each attack can be modeled as random noise, transmission errors, or other external effects would impede the flow of traffic. Security simply provides a more common vernacular for discussing transmission issues. It's also easier to reason about adversarial attackers rather than electrical interference. By translating the problem into a security one, we can model all these affects as "bad people" and it is a lot more fun to slay dragons, than it is to protect against some amorphous something. 

Okay, but what does this have to do with testability? Ah. It's subtle, but the same process we took to make our protocol secure also made each step verifiable. For instance, the final verification step could have been as simple as Bob sending an ACK that he verified the document's signature. This however isn't secure. An ACK can be faked, or replayed. Instead Bob build a cryptographically secure signature for Alice to verify. From a tester's perspective Alice is the "verifier", and Bob generates test data. Bob cannot be trusted to verify something himself, the test must generate auditable output. Thus the same process which drove us to make a secure response, also generated a auditable one for the tester to report. Thus security is more useful than simply protecting our data, it helps us design better products. 
