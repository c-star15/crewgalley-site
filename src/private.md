---
title: Private by design — Galley
description: Every Galley message is end-to-end encrypted on your phone. We cannot read your chats, and neither can anyone who gets into our servers.
---
# Your messages are yours

<p class="lead">Every message on Galley is encrypted on your phone before it leaves it, and only the people in the conversation can open it. We can't read your chats. Neither can anyone who breaks into our servers, and neither can anyone who asks us for them.</p>

<div class="grid">
<div class="card"><strong>Invites</strong>How you reach someone new: a plan and a time, no text, so there's nothing to read. If they say yes, the chat opens, encrypted from the first word.</div>
<div class="card"><strong>Chats</strong>Every message after they accept. Encrypted, every one.</div>
<div class="card"><strong>Meetup chats</strong>The group chat for a meetup. Encrypted for the people going, and closed 24 hours after.</div>
</div>

## Why it matters to crew

You talk about where you are, when you land, what you're doing tonight. That's nobody else's business: not ours, not an airline's, not a hacker's. Crew deserve to talk to crew the way they would in the galley, without wondering who else is reading.

## How it works, in four steps

1. **Your phone makes its own key** the first time you sign in. It stays locked in your phone's secure storage, is never sent to us, and can't move to another phone, not even through a backup.
2. **Every message gets a fresh lock.** Your phone encrypts it with a new random key, then locks that key separately for each phone in the conversation.
3. **We carry sealed envelopes.** Our servers store and deliver the locked message. Without a phone's key there is nothing to read, and we don't have any phone's key.
4. **Their phone opens it.** Only a phone that was in the conversation when the message was sent can unlock it.

## What we can see, and what we can't

We would rather tell you than have you find out.

**We can't see** what you write: chats, meetup chats and any older requests are sealed on your phone.

**We can see** what it takes to run the app:

- that a conversation exists, between whom, and when messages were sent
- how many phones you use and when each last opened Galley
- roughly how long a message is
- the "Up for" chip a request came from (coffee, dinner…)
- invites: who, the plan, the day and time of day, and the answer (invites contain no text)
- when you send an invite to someone who takes them only from crew who've landed: the city your phone says you're in, for 12 hours. Your phone does the check; we never get your location
- meetup titles, neighbourhoods, venues and times, because they're posted to the board
- your profile and stays, because that is how the board shows you to crew who overlap you

## If something goes wrong

Because we can't read chats, we only ever see what **you** choose to show us. When you report someone, the app offers to attach your recent messages with them. It opens them on your phone and attaches each one with the single-use key that unlocks it, so our reviewer can check every attached message against the sealed copy on our server. That means a report can't be faked or edited, and nothing else in the conversation is ever opened.

## What this means for you

- **A new phone starts fresh.** Messages are locked to the phones that were in the conversation. On a new phone you'll see new messages; older ones stay on your old phone. Chats on Galley are short-lived anyway: invites expire at the end of their day, meetup chats close after 24 hours.
- **Deleting your account deletes your keys:** the phone you delete from erases its private key and we erase every public key. What's left on our servers can no longer be opened by anyone. Other phones signed in to the account keep their key until you remove the app.
- **Your data export** (You → Settings → Export my data) opens the messages you sent on your phone and saves them as text. We never see that file.

## If someone asks us for your messages

We can only hand over what we have. For messages that is sealed ciphertext we cannot open. We answer only valid legal process, and we would rather have nothing to give.

## For the technically curious

- **Algorithms:** NaCl. Messages use XSalsa20-Poly1305 with a fresh 256-bit key and nonce per message. That key is sealed for each recipient phone with Curve25519 key agreement and XSalsa20-Poly1305.
- **Keys:** one Curve25519 key pair per phone and account, generated on the phone and stored in the iOS Keychain (this device only, never synced to iCloud) or, on Android, encrypted with a key held in the Android Keystore. Only the public half is registered with us. Up to five phones per account.
- **Authenticity:** every message is authenticated by the sending phone's key; a changed byte or a swapped sender fails to open.
- **Server checks:** the server can't read messages, but it refuses ones that aren't addressed to the people in the conversation, or, in a one-to-one chat, that leave out the other person's phone.
- **Tested:** an automated test runs the app's own encryption code on every change to it: sealing, opening, tampering, impersonation, new phones and report keys.
- **What it doesn't do yet:** there are no security codes to compare with the other person in person, and keys are long-lived rather than rotated with every message as Signal's are. Both are on the list.

Questions: [privacy@crewgalley.app](mailto:privacy@crewgalley.app).
