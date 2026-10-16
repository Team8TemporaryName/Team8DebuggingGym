# Week 2 validation meeting transcript

**Date:** 2026-10-14
**Participants:** Magel0n, Customer, Tedor49, NikitaRUniverse, Doosuur14

[00:00:00] Magel0n: Excellent. And lastly, can we share it privately with the instructors if publication is refused?
[00:00:08] Customer: Yes.
[00:00:10] Magel0n: Excellent.
[00:00:17] Magel0n: So without further ado, let's start. Our problem space is that the software developers and programming language learners want targeted, hands-on practice that trains a specific debugging skill, but the existing platforms offer general exercises rather than experience for a particular kind of debugging program.
[00:00:37] Magel0n: So, to settle our prototypes, to understand what is happening and to communicate with you, we have developed a prototype. So right now we would like to know if it was correct or right and to debug it and to check what looks well and not. And to settle the boundary and the minimal usable product candidates that they are all correct. So would you please take over and show the prototype?
[00:01:18] Tedor49: Okay, so give me a second.
[00:01:26] Tedor49: I thought I would have a little bit more time.
[00:01:32] Magel0n: If you need more time, I can, for example, discuss about our decisions regarding the previous meeting and like the constraints that we have.
[00:01:40] Tedor49: No, no, it's okay. Let me share this. We have this VS Code client with some buggy program, and this buggy program is sourced from a server. where the only thing that the user needs to connect remotely is this visual code launch configuration after which it can after which they can well just use the vs code buttons to attach and then we can start debugging session like this. It's run all the way through right now and it's gone into the harness. 
[00:02:40] Tedor49: You can see some debugging information here, but this is not the point. The point is that we can put breakpoints. If only I could click. This will be okay. Then we can
[00:03:00] Tedor49: attach and then we can do the same thing again, debugging. Now we are on this line and the code is running on a remote server, not on our system. Then we can look at debugging information. and then we can like continue so in this test and it prints our passes and fails right now so the bug in this code is that we do not iterate all the numbers and it's supposed to return the average of all numbers verse so we can see that here well one of the test cases is one two three so we can continue oh Okay yeah I think I continued too much little bit but well it also shows us the 
[00:03:59] Tedor49: the expected and actual results that we get from our programs
[00:04:06] Tedor49: programs and then it shows us that we have failed and this will need to be removed but this is a prototype okay and so then we can try to change the program then we will need to push it back to the server this does not work well right now But then we can attach to debugger again and you can see all the test cases have passed and this code runs on a remote server, not an ARM machine. So the biggest pain point from previous week, which is, are we able to remotely debug? It is possible to remotely debug. I think this is all for the prototype.
[00:05:10] Customer: Okay, thank you. i think if you need my feedback then please show the i keep showing the prototype um i'd like to see its parts in more detail and discuss them okay uh so where is the code stored
[00:05:41] Tedor49: Well, the code is stored on the server, but VS Code, when it attaches to a remote session, creates a copy in your own environment. But the code that is executed is stored remotely.
[00:05:56] Customer: You mentioned that pushing something to the server, what do you mean?
[00:06:11] Tedor49: So you see if I for example if I reintroduce the bug right now and I just try to debug it again then it will still pass because these changes are not synced automatically right now and we plan to address this in the minimum value product all right
[00:06:33] Customer: Okay
[00:06:45] Tedor49: And also this proves that the code that is running is not on our machine since we have changed it and the result did not
[00:07:00] Customer: Right. I mean, this code is on your machine, but there is another copy on the actual server.
[00:07:07] Tedor49: Yes, exactly. 
[00:07:08] Customer: Okay. So, which VS Code is this? Is it a standalone application or in a browser?
[00:07:19] Tedor49: This is the standalone application. 
[00:07:25] Customer: Okay.
[00:07:29] Customer: Did you think about moving it to the browser? Maybe it will open from the side. Are there any obstacles to this?
[00:07:41] Tedor49: We will need to see how it works in the browser and what kind of file storage is there, but I think it will work. But then we need to do it with actual IPs and not just getting everything on localhost.
[00:08:01] Customer: All right. So you think files will still need it to be stored somewhere?
[00:08:16] Customer: so if they uh i'm not sure how github code spaces works then do they store files in your browser somehow or
[00:08:32] Customer: or store them in the repo and then your vscode magically gets access to them
[00:08:38] Tedor49: yes we will need to research that exactly
[00:08:45] Customer: okay uh so nice you you have this buggy program um and you can trigger bug using the harness
[00:08:55] Tedor49: Yes so this is the harness
[00:08:58] Customer: Can you show it?
[00:08:59] Tedor49: yeah this is the harness it just has some test cases and then it just can run all of them in sequence sequentially and so this output is actually from the harness itself
[00:09:19] Customer: Okay, seems reasonable. So how do you think should the harness be modifiable file?
[00:09:34] Tedor49: It shouldn't, and we should definitely fix that.
[00:09:44] Customer: Why do you think it shouldn't be?
[00:09:47] Tedor49: Because I think the exercise, it needs to have a set success state. So if we can change the success state, then who's to say we don't just tell us we succeeded and go on with our lives. So I think the part that checks whether we have fixed the bug shouldn't be modifiable.
[00:10:07] Customer: Okay, I agree.
[00:10:24] Customer:  I'm not sure how it can be implemented in VSCode, but I hope you figured this out.
[00:10:34] Customer: Okay, so there is launch.json. What's in there?
[00:10:39] Tedor49: This is a standard VS Code launch configuration so that this appears in here and we can just press a button to start a remote debugging session. and this is a prerequisite to start debugging but i think and we will need to provide a way to download it somehow so here it just says where to connect to our server that we try to that it's not another device and it's a remote device and where we copy the code
[00:11:24] Customer: Okay. So is this configuration expected to be static?
[00:11:38] Tedor49: Yes, it is. 
[00:11:40] Customer: For this debugging session?
[00:11:41] Tedor49: Yes, it is. 
[00:11:46] Customer: So it won't need to change?
[00:11:48] Tedor49: No, it will not need to change.
[00:11:57] Customer: Uh maybe provided not via a file somehow an alternative is VSCode extension
[00:12:05] Tedor49: yes we plan on doing something like that oh oh but well this is this is a very minimal prototype just for the riskiest part
[00:12:15] Customer: sure yeah 
[00:12:23] Customer: so the triggering bug works and fixing bug leads to all tests passing right but uh i can't really see ah so they're there in the debug console
[00:12:39] Tedor49: Yes
[00:12:44] Customer: so the person should Be somehow instructed to open the debug console
[00:12:48] Tedor49: the debug console is opened automatically when you launch a debugging session so i think they more need to be instructed to look at it
[00:12:56] Customer: Uh right uh maybe uncollapse this part of the screen yeah uh what about um how do you ensure that the person starts a debugging section
[00:13:22] Tedor49: Well, we need to instruct them somewhere, maybe on our online website, when we will have one, or a teacher can do it. but since we are targeting people that kind of already know some programming so that they can debug I assume that they will be a little bit familiar with some IDEs and so they can understand how to launch a debugging session
[00:14:07] Customer: okay but some people may debug without a debugger we just read the code interpret it in their mind in their head and then fix the problem how should they know that where can they see the test results
[00:14:37] Tedor49: What I know for this kind of debugging in my own experience is that, well, you still need to launch the code to check if it is correct. And here we are just asking the user not to press the launch code button, but the attached to debugger button. So I don't think this will be a very big issue. as we can we can also perfectly print the bug this code right now because we can just not use breakpoints
[00:15:22] Customer: Uh but so how do you run this code like as a user um yeah i mean there is a single function uh well okay okay should this be up to the user to write some additional code to debug as they want like maybe some print statements Or should we provide some main?
[00:15:42] Customer: What do you think?
[00:16:01] Tedor49: It's a good question. I don't think we can come to a solution since I don't think it's that important than the different platforms where you upload code to do different things like LeetCode. It just has the functions. that are tested independently without any main and like Codeforces has you submit like full programs. I think for our purposes we We can just stick with functions since our primary purpose is to check whether the person has successfully fixed the bug. I do not think the user would need to launch the code in a different context.
[00:17:06] Customer: But so are they able to run this code at all like without harms
[00:17:16] Tedor49: Oh yes
[00:17:21] Tedor49: Like oh okay uh they probably can be just this no well right now they can do it just because the code is very simple uh but uh uh i don't know how it should work for the final version uh what do you think
[00:17:46] Customer: Uh i think they they should be able to to use any provider tools to debug the program including running the program with print statements maybe so right now they can open the terminal write python uh i guess minus m up dot buggy program dot Or something like this.
[00:18:16] Tedor49: Well, they can since the code is mirrored to their device. I was more thinking of something inside, well, VS Code itself.
[00:18:33] Customer: I don't know. 
[00:18:37] Customer: I think Python has dog tests or something. like some tool to run code inside doc strings i'm not sure like haskell has it so maybe they can there can be some comments inside the code working where they can press a button and run some line of code to see the output but i think this this is not very convenient and they will see the output inside comments i think a better better solution is to let them run on the terminal or provide some button to run this whole module so if if you build an extension there should be at least like two buttons to run a module and to attached to the debug session maybe to also to reconnect to the server the short button um and maybe some instructions on what each button does and like what is expected uh from this program uh i mean the the this box strings inside the function explain what this function does but what if there are multiple functions where can the user discover the task that they need to solve i think it should be somewhere near the program so that the user doesn't need to switch to another window to go to the site and see the original task again what do you think
[00:20:43] Tedor49: Oh yes i think this is very reasonable or we can add the task just to the top of the top of the file and also to extension but well we will need to do that in the future yeah or consider maybe if it if you come up with better design uh we'll let you know
[00:21:02] Customer: yeah but i think Having a task statement somewhere in the IDE might help the student keep the focus on the task and navigate this program better. OK. So breakpoints work. Uh-huh. So this program has a single module. Should we support multi-module programs, do you think?
[00:21:59] Tedor49: I think we should since it more accurately will reflect actual production environments and technically they in in this very simple prototype they are already supported since the harness is just another module which calls the buggy program module
[00:22:23] Customer: right um hopefully the harness does not have bugs um
[00:22:37] Customer: How can we ensure that that's a discussion for another brainstorm probably like what do we do with harnesses how do we test them should we discard bad harnesses but it's worth thinking about Should students be able to report bad harnesses? And so on. Bad harness may misbehave, like the whole memory. As I understand, it runs on the student's device, right? The student's computer.
[00:23:28] Customer: Does it?
[00:23:29] Tedor49: Could you please repeat the question? 
[00:23:33] Customer: Does the harness run on the student's computer?
[00:23:35] Tedor49: No, it does not. It runs on the server. Everything runs on the server.
[00:23:43] Customer: Ah, okay. So the student can't... Okay, which... For example, if a student wants to profile the program... how do they get the tools to profile it or to run commands um inside their id so does the terminal have the same environment as the server
[00:24:17] Tedor49: I think it would have the same environment uh maybe with even with some like uh maybe with a limited amount of test cases but uh the server should probably have some test cases that the personal environment does not have
[00:24:42] Customer: uh okay might be the case like hidden tests something Okay, but what about the terminal? Which environment does it have now? Is it connected to the server? Does it run inside the server, kind of?
[00:25:00] Tedor49: I don't think so.
[00:25:05] Customer: So if I want to use some linter or typeshaker and I don't have it installed in VS Code, what do I do? Should I install it on my machine or can I use some tool on the terminal or can I somehow receive the diagnostics from the server?
[00:25:36] Tedor49: I think, well, if you want to use a linter, then it would probably be more idiomatic to download your own linter. But we can definitely add support for different checks, not just that the code runs correctly. and as for will the tools for these checks like like if we require our like if we require like with some of our own linting rules i think these tools should be provided well by the extension and they should be installed automatically with the task
[00:26:07] Customer: Um yeah i think i agree here uh so uh one more question so you right now accept any um any code from but from the buggy program on the server i mean until you run it
[00:26:58] Tedor49: yes so obviously it will need to be sandboxed and probably virtualized as well 
[00:27:10] Customer: yeah maybe it can also be inspected using an agent but yeah but it will increase the cost of operating this this whole system Okay, so my initial assumption was that both programs and harnesses are written by agents. Can they be authored by humans? What do you think? Should they be authored by humans too?
[00:27:52] Tedor49: Are you asking if the humans should be able to create their own harnesses?
[00:28:01] Customer: Yes, not the students, but task creators.
[00:28:06] Tedor49: I think yes, because I think if you would be willing to create a harness with a virus by hand, then you can force an AI to create a harness with a virus. So I don't think it will introduce many more problems.
[00:28:29] Customer: Probably there should be some moderation system on the side so that you can remove malicious tasks and so on. Monitor how the harness behaves at runtime. Maybe it eats the whole memory, so it should be replaced. Okay. I can't come up with more questions right now. Maybe you have some questions for me.
[00:29:27] Magel0n: Yes, we actually do have some questions for you. So, well, first of all, is this the general setup that the learner would accept, like with the attachment of the VS code?
[00:29:58] Customer: Is there any sticking points that stick out to you uh-huh where they can get stuck so um yeah so if all these files are i mean both files are opened automatically after connecting to the server and they there are understandable instructions in the sidebar somewhere else on what to do then i think the learner won't get stuck really they may get stuck when they need to install the extensions but as we discussed you you might probably somehow install the necessary extensions or prompt to install necessary extensions when providing the task to the user maybe provide the file with the recommended extensions but it's a technical issue maybe there are more elegant ways other places so if the user knows like step by step what they need to do and when can when can they know how can they know that they succeeded with the task then they probably want to get stuck also there should be instructions on what to do if the server has disconnected for some reason Maybe you see some points where they can get stuck.
[00:31:42] Magel0n: Well, as of right now, all of the points were already discussed by Tedor49 that we have found, and I think we will find more whilst we'll be implementing it. 
[00:31:57] Customer: Right. Okay.
[00:32:01] Magel0n: Is there something that would make you trust the harness's pass-fail signal?
[00:32:09] Customer: Sorry? Could you please repeat?
[00:32:13] Magel0n: One of the things that we were wondering if the trust in the harness's pass-fail signal is a question.
[00:32:26] Customer: I may mistrust the harness as a student. Yes. Or what? Okay. But why should I? I mean, by modifying my program, I can trigger some problem in the hardness, and then the signal will not be determined by the logic put into it by its creator, but it will be modified by my program. So... So if I see some exception, like some unexpected behavior of the harness, I can get confused. Why did it happen? And so at that point, I will think that the harness is wrong and it's doing some wrong thing. And I won't probably see that the problem is on my side. For example, the harness accesses the short element of list, but I made my list with only two elements. And then the harness throws an exception, and I don't see the expected yes or no result. Then I can get confused. What should I do in this situation? I can't fix the harness and I don't get any guidance from it because it just throws an exception. I'm not sure.
[00:34:28] Customer: Maybe I should ask my agent. Answering how we would make more trust in the harness is perhaps some sort of checker of the harness itself.
[00:34:43] Customer: Well uh this can continue to infinity like checker of checker uh yeah we need some guardrails for her for producing harnesses like whether they are written by agents or humans ideally they should be robust enough to handle uh like unexpected code or some class of expected code changes like we can't prevent them from throwing on like arbitrary code changes in the task module but at least we can handle some classes of problems
[00:35:40] Magel0n:  so okay so should we go for the next questions i'm trying to speed up a little
[00:35:48] Customer:  yes okay i'm sorry i think i think i have some idea not sure if it's implementable really so we have this program and we know where exactly the bug is uh and we know how to fix it uh so we can probably at the creation time uh compute the possible blast radius of this change so like we need to make this array like three elements long uh i mean the blast radius with respect to the ast of the code And then when the student changes the code at very unexpected places, then we don't accept this code. It's like a warm and cold game. We can guide the student towards the piece of code that they should look at. Maybe something like this may act as a guardrail towards very unexpected changes.
[00:37:08] Magel0n: Okay, let's proceed. So, is debugging in the user's own VS Code still the right priority given what the prototype shows?
[00:37:25] Customer: I think this code is a very capable IDE. And so yeah, let's keep it as a debugging tool, debugging environment.
[00:37:38] Magel0n: Excellent. May I then talk with you about the decisions that we have made and then to the constraints and the boundaries that we have just devised?
[00:37:48] Customer: Yeah, sure. 
[00:37:50] Magel0n: So, for the decisions, the first one is that, well, debugging in the user's own IDE is the first priority.
[00:37:59] Magel0n: Secondly, we target...
[00:38:02] Customer: Okay, not in the IDE. I mean, the VSCode installed.
[00:38:08] Magel0n: Yeah, but in a sense that users do everything, like, on their machine.
[00:38:16] Customer: Like local debugging experience, basically. Yes. But there is an open question, should this happen in the standalone application or inside the browser?
[00:38:35] Magel0n: Yeah.
[00:38:37] Customer: So we keep it open for now. uh i mean this question whether this should be a standalone application or browser yeah this is open but debugging of lock and having files available locally is closed like yes the user should have the files available locally 
[00:39:02] Magel0n: okay then the target is the Like a university students and like non-beginners basically not being complete beginners as we have discussed 
[00:39:17] Customer: uh yes
[00:39:21] Magel0n: uh okay and the problems are self-contained and reproducible on the provided virtual machine
[00:39:34] Customer:  uh yes no flaky harnesses 
[00:39:39] Magel0n: yeah yeah okay uh then uh based on that we have already devised our constraints and our boundaries obviously and among the constraints the first one is that the exercise environments run on a university virtual machine with like 16 gigabytes of ram and eight CPUs
[00:40:04] Customer: Yes for this project um i'm pinging the it department but they don't reply for several days so yeah unless um if they don't provide this virtual machines then the the server should be runnable locally luckily i think it's possible right now
[00:40:35] Magel0n: Okay. The API key budget is like $5 to $10. 
[00:40:46] Customer: Yes. 
[00:40:46] Magel0n: Okay. The in-environment agent must coach the learner, not solve the exercise. 
[00:40:58] Customer: That's right.
[00:41:00] Magel0n: And every exercise ships as a self-contained reproducible unit.
[00:41:12] Customer: Yes. 
[00:41:13] Magel0n: Excellent. Then for the boundaries, the first one is to host a fixed catalog of hand-curated problems. The second one is to run code in a browser editor or in the IDE itself. Third one is to run mock interviews or human-reviewed debugging sessions, perhaps, as we have advised before, and even host debugging Q&A.
[00:41:44] Customer: So that's what you're not going to do or what you're going to do?
[00:41:51] Magel0n: Well, we are hoping that this is, like, the next step after, like, we are not planning to do it, but this is what we're going to do. Like, this is... uh how should i put it future work basically yeah okay i agree uh to the same boundaries come like host debugging q a so that somebody could use our thing and uh debug it then we perhaps we could uh expand to teach programming from scratch and provide lessons, modules, or even certificates.
[00:42:09] Customer: Yes, this is not your responsibility for this project.
[00:42:41] Magel0n: Excellent. Now, so, no, the elements were wrong. And so we should not teach complete beginners. Or should we try to include complete beginners as a target?
[00:43:05] Customer: Define complete beginners.
[00:43:07] Magel0n: Somebody that is practically, like, it's their third time seeing code. 
[00:43:17] Customer: Mm-hmm.
[00:43:19] Magel0n:  I understand that ultimately we will not be able to guide them completely towards the system, but perhaps we should accommodate for their existence.
[00:43:37] Customer: Yeah, basically you should assume that... Okay, they saw the code. They know it can be edited. They know how to type and they know how to read instructions. I think instructions for users should assume that users are not very patient, very attentive readers. And then you can target the beginners too. The instructions for what to do in the system should be very clear, precise, concise. And then I guess even beginners will understand.
[00:44:31] Magel0n: Okay. They will. Then I would also like to run our user stories that we have prepared. So the first one is, as a learner, I want to pick a name debugging problem kind and get a fresh exercise for it so I can train the specific skill I am weak at.
[00:45:02] Customer: Sounds good. Yeah, it doesn't anchor the design.
[00:45:07] Magel0n: Yep. Second one. As a learner, I want to see the list of debugging problem kinds the site supports so that I can choose what to practice.
[00:45:24] Customer: This is a bit technical story. Maybe as a user, I want to be able to choose. or what what what could you choose from list what to practice what so it couldn't exercise yeah Okay, so as a learner, I want to choose an exercise that I don't practice what I've already completed, something like this, or what I already saw, or so that I improve my skill in a new environment.
[00:45:41] Magel0n: Okay. So you asked us to change that a little bit to that. 
[00:45:51] Customer: Yeah, I mean, it might be a list, might be a grid or some other implementation of a list. You should capture the intention of the user in the user story and the value.
[00:46:20] Magel0n: Okay. Next one then.
[00:46:51] Magel0n: As a learner, I want to open the exercise in my own VS Code so I can debug it with the tools I already use.
[00:46:52] Customer: Yes, since we have already settled that we're going to use VS Code, this can be that specific. Yes, or to debug in a familiar environment or to debug using the tools I already know.
[00:47:27] Magel0n: Yeah something like this okay moving on as a learner i want to run the exercise harness against my fix so that i know what the bug is when the bug is actually done uh
[00:47:47] Customer: So as a learner, I want to check whether I fixed the bug so that I know when I'm done with the exercise.
[00:48:03] Magel0n: I mean... Should we prioritize completing an exercise or fixing the bug?
[00:48:17] Customer: Completing the exercise versus fixing the bug so there are two escapes from an exercise like early exit and fixing the bug or crashing the server which is equal to the early exit i think the the main intent is to fix the bug not to edit the exercise early and finish it, I mean.
[00:48:54] Magel0n: Okay. So next user story.
[00:49:02] Magel0n: As a learner, I want full debugging features, breakpoints, stepping, stack traces, variables in my own editor so that I practice matches how I debug real code.
[00:49:29] Customer: Yes. Or so that I can debug my code using specialized tools, something, no.
[00:49:37] Magel0n: Like the idea is primarily to match what we do in the debugging real code and the practice.
[00:49:51] Customer: Right. Okay, let's keep it formulated like this.
[00:49:55] Magel0n: Yeah, I like it. Okay. Next up, as a learner, when I am stuck, I want an agent in the environment to guide me toward the bug so that I learn the skill instead of having the answer handed to me.
[00:50:15] Customer: Yes.
[00:50:30] Magel0n: Then, as a learner, I want to browse the public gallery of generated exercises so that I can practice a wider variety of problems.
[00:50:52] Customer: Uh so this is this one is very similar to what we had before like i want to to select an exercise that i don't practice like the same environment in the same stuff
[00:51:05] Magel0n: We tried to separate them based on one being more over how it should look and like towards the listing and whatnot. And the other one about just overall having the generated exercises somewhere. Plus the browser capability.
[00:51:24] Customer: I'm not sure i understand the distinction between the list and the gallery right now um yeah but okay 
[00:51:42] Magel0n: well if you don't understand the distinction perhaps this is an unnecessary user story then
[00:51:50] Customer:  it might be like what we we should i think the the public gallery should exist uh why should it exist so maybe like i want to i want to as a user or the student i want to choose exercises from a like public pool of exercises so that I can solve the same problems that my friend solves, for example, right now. So that we can try to debug it together or discuss the debugging process. Basically, yeah. And as a teacher, I want to select exercises prepared by someone else so that I don't spend time writing them on my own. Maybe something like this. And this will justify the existence of a gallery that contains exercises prepared by someone.
[00:53:15] Magel0n: OK, thank you very much. We will add it later. uh last user story then okay as a learner i want to practice in several languages python typescript java so that i can train the language i actually use uh yes i mean uh i want to
[00:53:24] Customer: I want exercises in the language that I actually use so that I can practice it. Maybe something like this.
[00:54:07] Magel0n: Okay, so more about availability and not putting it as in several languages.
[00:54:10] Customer: Well yes like i i want to yeah i want to solve exercises uh in my language that you can practice yeah but then we have a constraint uh on the supported languages uh but this is like outside the user story can be specified later like in the actual implementation
[00:54:48] Magel0n: Okay, thank you very much. That is it for the user stories. Now, if we can only build the candidate stories, can a learner complete the core task and what is missing if not?
[00:55:15] Customer: Which stories do you consider for a core task?
[00:55:20] Magel0n: Well, if we build based off all of these user stories to try to satisfy them, is there anything else missing?
[00:55:23] Customer: o all these user stories combined serve some core task? 
[00:55:23] Magel0n: Well, more or less, no?
[00:55:36] Customer: uh i mean yes but uh well okay the public gallery may serve such a core task but as for a usable product version it's not very much required to have like real public gallery it may be like a single account um site and the user will just choose exercises from a given list. So this will demonstrate that the user can complete a single task, core task. I think this set can be reduced a bit.
[00:56:47] Customer: Um and i'd like to hear like which user stories you consider for for a core task
[00:56:54] Magel0n: well we believe the core task to be for the user to uh have comfort in learning how to debug their programs and uh well we have created these user stories with the intent of them being complete and will If you think that some of them might be omitted, then please tell us which ones.
[00:57:16] Customer: Okay, so you should consider the core task. And the user should not get frustrated while completing this task. So, okay. uh you have user stories about uh like several programming languages and about the gallery um as a court task may be debugging a program in python like without even login on the site so something like what you demonstrated but like the whole flow that works and does not cause a frustration uh like this bug where you can't send locally modified code to the server or you can modify the harness so that it doesn't work um
[00:58:32] Customer: So yeah i suggest that you like make the set of stories a bit less ambitious and then you will arrive at a minimal usable product like more easily
[00:58:46] Magel0n: okay uh so which story then you could pull out of the can like you you believe that the like the different languages can be pulled out
[00:59:05] Customer: What was the other one?
[00:59:08] Magel0n: Public gallery.  So, any verdicts on the candidate?
[00:59:36] Customer: okay so so you should implement the core task like go to the site get the exercise uh connect somehow to the server and sorry go to the site connect somehow to the server and get the task probably in the IDE together with like during the process of getting the task and then like solve the task to bug the program get the verdict from the harness that the program is solved and then finish and then I don't know either go to the site again to see the verdict on the side like this problem counts are solved um yeah i think that this is like a logical engine you should not get stuck in the idea and this will be like the core task okay uh then do you have any extra questions yeah how did you implement the environment containerization on the server did you use docker
[01:01:13] Tedor49: yes we use the docker for the server 
[01:01:20] Customer: so you'll have in future you will have some containers with some specific tools or specific languages right 
[01:01:32] Tedor49: probably yes
[01:01:36] Customer: okay what if okay this may be like very far future but what if the task also wants to supply own tools in a container how do they do that
[01:01:55] Magel0n: What do you mean by their own tools?
[01:02:07] Customer: I assume that there will be some registry of docker files that you use to build containers. What if a task author wants to supply 
[01:02:42] Magel0n: Well, for now, it is a little too early in development to say for sure. but overall uh to avoid any malicious actors i believe we will have to either deny that possibility or restrict it heavily
[01:03:01] Customer: yeah probably yeah you don't want bad actors provide malicious software in containers
[01:03:17] Magel0n: Perhaps another option that we can try to implement is to allow them to connect their own servers so that we could transfer their own Docker images on their own server so that a user would transfer it to them directly. But that is not among our first priorities.
[01:03:19] Customer: Yeah they can host the site on their own if they really want to so okay let's not give them give like regular task creators options to modify the in the containers in any way so that we can control what's running on our server Yeah, I think that's it for now. Okay.
[01:04:21] Magel0n: Does anyone have any extra questions?
[01:04:30] Magel0n: Tedor49? Tedor49 is telling me that he has no extra questions. Well, for the note-taking, we have the recording. Well, I think then the meeting is over. Thank you very much for your time.
[01:04:49] Customer: Yeah, thank you for scheduling, continuing to meet.
[01:04:53] Magel0n: All right, then. Have a good evening. Goodbye.
[01:05:01] Customer: Yeah, you too.
