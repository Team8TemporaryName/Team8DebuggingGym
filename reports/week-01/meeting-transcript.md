# Kickoff meeting transcript

**Date:** 2026-10-02
**Participants:** Magel0n, Customer, Tedor49, NikitaRUniverse, Doosuur14

[00:00] Magel0n: Secondly, may we quote you in public research architects?
[00:09] Customer: Sorry, I couldn't hear you well. 
[00:11] Magel0n: May we quote you in public research archifacts?
[00:17] Customer: Yes.
[00:20] Magel0n: And can we name the meeting in the week report?
[00:25] Customer: Okay.
[00:29] Magel0n: So, thank you very much for coming. 
[00:37] Magel0n: Well, how should I start?
[00:43] Magel0n: We have checked the alternatives on the market.
[00:48] Magel0n: We have seen other options like CodinGame, LeetCode and Rustlings.
[00:54] Magel0n: We have devised their strengths, weaknesses, some of our observations.
[01:00] Magel0n: All of this you can find on our repository. 
[01:12] Magel0n: And we have devised that there is a research gap with the target audience still needing to train that programming skill of debugging but with a deployable version where you could try on your own VS Code and see it helping you lock to a separate like hosting and lock to some of the other things like use code, request from your own thing.
[01:45] Magel0n: Actually there are some of the other things like
[01:49] Magel0n: I'll try not to be too frantic.
[01:53] Magel0n: Basically, what we want to do is to create this problem automatically and have an extra element of openness with the picked out solutions and questions to further support the system.
[02:15] Customer: Yes, something like that.
[02:18] Customer: Sorry for interrupting you, but I can hardly hear what you're saying.
[02:23] Customer: Maybe you should direct your words at your mic, I don't know.
[02:33] Magel0n: Well, I am... 
[02:35] Magel0n: Give me a second I'll try to fix this
[03:02] Magel0n: Greetings. 
[03:06] Customer: Hi. Okay.
[03:08] Magel0n: This should make it easier.
[03:12] Customer: Sounds much better.
[03:14] Magel0n: Sounds much better?
[03:15] Customer: Yes. 
[03:19] Magel0n: Where were I?
[03:22] Customer: So you compared some competitors.
[03:26] Magel0n: Yes, precisely. 
[03:27] Magel0n: And we have devised our own analysis, but today we have a goal of understanding where we got it wrong and where we need to design something differently from your perspective.
[03:39] Customer: Aha
[03:42] Magel0n: So, primarily, I believe we need you to answer a couple of our questions.
[03:48] Customer: Sure.
[03:50] Magel0n: Do you have any questions of your own, like regarding gap analysis and whatnot?
[03:55] Customer: Yeah, maybe you already found some solution that pretty much covered the stated problem, did you?
[04:07] Magel0n: Well, as I said, we have looked at the alternatives, which are CodinGame, LeetCode and Rustlings.
[04:15] Magel0n: We have not found anything else closer to what we were searching for.
[04:24] Magel0n: An alternative that still needs to be created, but it's from a different company, is LeetCode.
[04:30] Magel0n: It's the closest, I believe, because they could try to generalize their massive database and try to change it.
[04:41] Magel0n: However, that will require significant effort from their part, and, well, they haven't done it.
[04:50] Magel0n: But other than that, well...
[04:53] Magel0n: We did not see any other alternative.
[04:59] Customer: Okay.
[05:00] Customer: I can say that Codeforces also has something similar.
[05:06] Customer: So they have contests, and after a contest you can hack someone else's solution.
[05:14] Customer: So come up with a legal test that will make the solution fail
[05:25] Customer: But you don't like observe everything I guess in on Codeforces you can't like really debug a program using the modern tooling like you can codeforces interface still need to load it into your idea.
[05:44] Magel0n: So well, that is another part of way, we're trying is to allow you to have it in your own Visual Studio Coding
[05:53] Customer: Okay so
[05:55] Customer: Okay, thank you for the analysis.
[05:59] Customer: For the competitors, we can proceed to the questions.
[06:03] Magel0n: Well, let's start with the business goals.
[06:06] Customer: Okay.
[06:07] Magel0n: What is the outcome that you want from a debugging practice tool to achieve for the students or developers, and how would you know it worked?
[06:21] Customer: Okay, this is a tough question.
[06:30] Customer: Maybe I will...
[06:33] Customer: If I use this tool with students, I can potentially conduct some exams, maybe paper-based, where they need to debug without this tool, and then I will see who is able to debug and who is not, whether they can spot bugs quickly.
[06:59] Customer: But for general audience, I can't guarantee
[07:04] Customer: There is no reasonable test that will confidently show that the person learned something, because they could ask an agent to complete the task for them.
[07:23] Magel0n: Well, thank you. Anything else?
[07:27] Customer: No, no. 
[07:30] Magel0n: So, another question. 
[07:33] Magel0n: Who in your world feels the pain of "I keep hitting the same kind of bug" most acutely?
[07:41] Customer: Could you please repeat the question?
[07:47] Magel0n: Who in your world feels the pain of "I keep hitting the same kind of bug" most acutely?
[07:53] Magel0n: I believe it was in the description.
[07:57] Customer: I don't get the verb.
[08:00] Customer: I keep hitting...
[08:06] Magel0n: I keep hitting the... hitting.
[08:09] Customer: Who in your world "I keep hitting the same bug" most acutely?
[08:15] Magel0n: Yes, we are trying to figure out who is the target audience precisely.
[08:27] Customer: Okay, I assume this might be university students.
[08:36] Customer: They have some courses on programming, and it would be nice if they have an opportunity to train their skills, like advance their skills.
[08:52] Magel0n: So primarily university bachelor students, masters?
[08:59] Customer: Depends on the program.
[09:02] Customer: Like if master students have to learn a new language, like they learn Prolog, then maybe the team might help them learn it more quickly.
[09:18] Customer: Or practice some advanced debugging topics.
[09:26] Magel0n: Do you have an age group, perhaps?
[09:31] Customer: Age group...
[09:36] Customer: So we might have a constraint that the user supplies the API key, like for a model to generate problems.
[09:48] Customer: So probably the user should be over 18 or like at which age they can legally buy API keys and so on.
[10:02] Customer: Like make any transactions, money transactions.
[10:06] Magel0n: Okay.
[10:10] Magel0n: And I would also like to ask, we assume that they are novices but not complete beginners in programming.
[10:20] Customer: I agree because this need to practice debugging would more probably appear in someone who is forced to practice debugging at the university or someone who likes programming so much that they want to practice debugging.
[10:49] Customer: The target users do have some experience with the languages that they want to practice. 
[10:58] Customer: Most probably.
[11:00] Magel0n: Alright.
[11:02] Magel0n: Okay, so would you rather see learning spend more time debugging or more skills per hour?
[11:11] Customer: Could you explain what you mean?
[11:15] Magel0n: I believe that you like to try to see the metrics, for example, in terms of the time they have spent debugging, the solves that they have created, or something like debugging different kinds of problems like the racing conditions and whatnot.
[11:40] Customer: Good question.
[11:44] Customer: If we measure just the time they spent debugging a single problem, should we also measure the time when nothing changes, like no commands run?
[11:58] Customer: Is it that they walked out of the home for a walk or they keep thinking about the problem and trying to solve it?
[12:12] Customer: I don't think it's a very good metric.
[12:17] Customer: Okay, regarding the diversity of problems solved, what was your alternative metric?
[12:29] Magel0n: Yes, for example.
[12:34] Customer: Yes, this might be a metric if it's tied to some goal.
[12:46] Customer: Like maybe the person wants to cover a topic like concurrency in Go and they solve problems that cover this topic.
[13:04] Customer: Maybe we can define some lessons that cover this topic and for each lesson define a problem or problem set and then we can see how many topics are covered.
[13:22] Customer: Not sure how to better implement this.
[13:31] Customer: If we use some other approach of coming up with problems, maybe some hard-coded prompts, then we can just measure how many of those prompts the person solved.
[13:48] Customer: How many problems the person solved.
[13:51] Customer: Honestly, I don't have a good metric in mind.
[13:58] Magel0n: Well, we'll try to just gather as much statistics and then we could perhaps try to figure it out once we have some tests.
[14:09] Customer: Okay.
[14:11] Magel0n: So then I guess we should move on.
[14:15] Magel0n: About the end users.
[14:18] Magel0n: When you imagine a learner using this, what does their current debugging session look like, like step by step?
[14:30] Customer: So first of all, they need somehow to get the code into their IDE.
[14:42] Customer: I have an idea about how they can do that.
[14:46] Customer: Is your question about how I envision the interface or how I envision how people debug usually, or what?
[14:59] Magel0n: How you would see a learner using this product.
[15:03] Customer: Okay, suppose we have some website where the learner can choose the topic for a problem or maybe some parameter.
[15:18] Customer: So they set the parameters and they hit like generate and the setup is generated.
[15:28] Customer: So one option is that this website will send them some link by which they can click and somehow open their IDE.
[15:43] Customer: And the IDE will have all necessary tools for debugging, like the terminal with necessary tools.
[15:56] Customer: If the problem is about golang race conditions, then there will be some Go compiler, a language server, that will start working when the person opens the problem code.
[16:14] Customer: Maybe some other tools like some profilers.
[16:21] Customer: Yeah, and most probably there should also be some agent in the environment that may help the person to run commands or like that will ask some questions to guide the person in the debugging session.
[16:39] Customer: And the person will run tests to see whether the bug is gone.
[16:49] Customer: So when a problem is generated, like the code for a problem is generated, both the actual code is generated, the code that contains the bug, and some harness is generated that helps observe the bug in some way, or observe the lack thereof.
[17:13] Customer: So the person can run that harness and see whether the bug is gone.
[17:18] Customer: And when they complete the debugging, they can run a command to finish the session.
[17:28] Customer: Maybe they literally run the finish command in the terminal and then the session is assessed somehow by the system, maybe some statistics is provided and the ID is disconnected from the service.
[17:52] Customer: After that, the person may go back to the site where they obtained the link and maybe try it again or maybe try some other problem.
[18:03] Customer: So that's that's the flow that i imagine right now i see
[18:19] Customer: One thing that can be simplified here is uh to provide with this code directly on the website so this feature is similar to what's on github so you go to a repository click dot on your keyboard and then code space opens like VS Code with some extensions installed and you can browse the repo using this VS Code.
[18:47] Customer: So maybe we can use VS Code or some other code editor with debugging capabilities to provide like this more seamless experience for user.
[19:01] Customer: So they generated like ask the service to generate the problem and setup and they can immediately open this code in the browser and start debugging.
[19:18] Magel0n: All right.
[19:20] Customer: That's it.
[19:22] Magel0n: What do your users do today when they want to get better at debugging?
[19:36] Customer: That's a good question.
[19:40] Customer: I don't know any users who deliberately study debugging.
[19:49] Customer: I haven't really seen such courses in our university.
[19:54] Customer: Usually, the users or programmers either contribute to some established projects on GitHub, report some issues, make some PRs, or they solve some little tasks on code forces or lead code.
[20:13] Customer: They write the solutions from scratch usually, but like deliberate debugging, I don't know how people learn how to debug outside some existing setting like some enterprise or a GitHub project.
[20:44] Magel0n: Okay.
[20:46] Magel0n: Coming back a little, because this is where it is actually written.
[20:50] Magel0n: So we will be expecting the users to more likely be students in the course, or should we also expect for some working developers or even some of the tests to be about general language learners?
[21:06] Magel0n: Just to repeat that question.
[21:09] Customer: Yeah, we can assume general audience, like people who know what debugging is actually, at least.
[21:27] Customer: But only for students can we really conduct some assessments, some exams, and see whether they learned anything.
[21:41] Customer: That's why I answered like this at the start of the conversation.
[21:47] Magel0n: Okay.
[21:50] Magel0n: Then coming back to the today question, are there any tools that are open?
[21:58] Magel0n: Like you have mentioned VS Code and other IDEs.
[22:03] Magel0n: Is there anything extra like a terminal?
[22:10] Customer: VS Code has an integrated terminal, and it can be used for running commands in the environment provided by the service.
[22:23] Customer: A language server is a tool that lets you see types of variables or go to a definition or see documentation for a variable or a function.
[22:40] Customer: Some VS Code extensions simplify the debugging process.
[22:46] Customer: They let you set breakpoints, step into functions, see the state of the program at some point.
[22:57] Customer: Yeah, I think that's enough for a start.
[23:07] Customer: Yeah, like the compiler, VS Code, language server, and some extensions in the terminal.
[23:15] Magel0n: What specific extensions do you remember, or are they just general?
[23:20] Customer: It depends on the language.
[23:23] Customer: So for Python, there is an extension from Microsoft, I guess.
[23:29] Customer: For Haskell, from Haskell Foundation.
[23:32] Customer: Okay, so the extensions are language specific.
[23:43] Magel0n: Okay, next question then.
[23:50] Magel0n: Where in the workflow of the students today that are trying to get better, do they give up or get stuck?
[24:04] Customer: Sorry, when do they give up?
[24:09] Magel0n: Give up or get stuck or otherwise fail at continuing their getting better at debugging?
[24:19] Customer: I don't really get this question.
[24:22] Customer: Like, what should happen when they get stuck?
[24:25] Magel0n: No, no, no, at which point they get stuck, yes.
[24:32] Customer: And what do you mean get stuck?
[24:36] Customer: Like, they can't finish debugging a program?
[24:40] Magel0n: I guess.
[24:42] Magel0n: They may give up in doing the program or sometimes like...
[24:52] Customer: Okay, honestly, I don't know when they get stuck.
[24:58] Customer: But there are several points where they can get stuck.
[25:03] Customer: First of all, they may not understand how to run the tests.
[25:07] Customer: They will not be able to discover the program that runs tests or this harness that shows the bug.
[25:18] Customer: Then they may get stuck when the memory of the container is exhausted, and the system becomes unresponsive.
[25:33] Customer: They may get stuck when the connection to the server is lost, or when the program runs an infinitely long time, they may not be able to kill it somehow.
[25:52] Customer: Yeah, but if they understand how to use the program that runs the tests, they may get stuck when they need to finish this exercise.
[26:07] Customer: They may not know which command to run in the terminal, or they may get stuck when they don't know how to debug and how to call an agent to help them.
[26:25] Customer: They may not know the command to run an agent or that they may not even know that the agent exists inside that environment, assuming that we provide such an agent, like open code.
[26:43] Customer: And after they finish, they may get stuck because they don't know that they need to go to the site and do something else there.
[26:55] Customer: So maybe some instructions should be given, like when they finish an exercise, then go by this link, for example.
[27:08] Customer: So these are places where I see a user might get stuck.
[27:15] Magel0n: So these are also the points where we could say are the most frustrating part of this practice, right?
[27:24] Customer: Yes.
[27:27] Magel0n: So is there anything extra from the instructor side?
[27:32] Magel0n: Any frustrating part of the current debugging practice from the instructor?
[27:40] Customer: Hmm.
[27:45] Customer: Okay, I'm not sure the sessions will be supervised by an instructor.
[27:55] Customer: So, not sure if they will feel any frustration at any point.
[28:02] Magel0n: I was asking about the current practice.
[28:05] Customer: The current practice?
[28:08] Customer: Okay, I did have experience helping students to debug their setup software engineering toolkit course.
[28:26] Customer: So probably the most frustrating part is to understand at which state the environment is for a student.
[28:42] Customer: But given our environment is pretty much invariable and it's pretty much simple, probably instructor will not have any problems with it, especially if they are proficient with the language and with the debugging process for programs in that language.
[29:08] Customer: What can frustrate them, though?
[29:13] Customer: Maybe some technical failure points that I mentioned, like disconnections, like telling the student to connect again, or um...
[29:29] Customer: Yeah, I'm not sure who is going to provide the API key, but if the instructor provides the API key, then the student may hit the money limit for that API key, and then this may frustrate the instructor.
[29:51] Customer: Maybe tracking the limits is necessary.
[29:55] Customer: I'm not sure.
[29:59] Magel0n: So... I see. Anything else?
[30:07] Customer: No, not really.
[30:11] Magel0n: I have one more similar question.
[30:15] Magel0n: When a learner gets a bug they cannot solve, what do they do and why does that fail right now?
[30:24] Customer: What do they do and why does that fail?
[30:29] Magel0n: Yes.
[30:30] Customer: Uh-huh.
[30:36] Magel0n: It's similar.
[30:38] Customer: Yeah.
[30:40] Customer: In the toolkit course, when they can solve a bug, they just prompt the agent more fiercely, until it solves the bug.
[30:49] Customer: Yeah, and what can fail is that the agent just tries, tries, tries, and then the context is exhausted and there is no result.
[31:02] Customer: Then the student gets frustrated that they spent 20 minutes watching an agent to debug.
[31:10] Customer: But, like, using an agent to debug a task is not the point of this exercise.
[31:26] Customer: So, I don't know.
[31:33] Magel0n: Well, maybe next question then.
[31:38] Customer: Okay.
[31:41] Magel0n: Is there any extra constraint that we should know about?
[31:43] Magel0n: Maybe class size, maybe environments have something, maybe tooling students are not allowed or allowed or forced to install.
[32:00] Customer: So you will probably get a virtual machine from the university, 16 gigabytes of RAM and eight CPUs.
[32:17] Customer: And that's all what we can provide right now.
[32:22] Customer: Like maybe the IT department can provide you more, but I haven't yet negotiated that.
[32:33] Customer: So, regarding the tooling for this project, I expect you to either use some container technology for this programming, debugging environments, like maybe Docker containers, or spin up some VMs, like using NixOS VMs.
[33:01] Customer: This might make the setup more reproducible.
[33:10] Customer: Other constraints.
[33:14] Customer: So I will not be able to provide you infinite tokens for testing purposes.
[33:22] Customer: Probably it will be an API key with $5 or $10.
[33:29] Customer: And I would recommend to use some cheaper models just for prototyping and testing hypothesis.
[33:43] Customer: Yeah, any other categories you mentioned?
[33:47] Magel0n: Originally I was questioning constraints regarding the students.
[33:51] Magel0n: Maybe the students have their own, like, they need to get this, they need to do that, maybe the class size once again.
[34:00] Customer: Oh, sorry, okay.
[34:08] Customer: For a student, the prerequisites should be minimal.
[34:15] Customer: They enter the site and then they somehow connect to the environment.
[34:20] Customer: And then in an IDE, they can debug.
[34:26] Customer: So one option is for them to have VS Code installed with some necessary extensions.
[34:35] Customer: Another option is to run VS Code from the browser where extensions are already pre-installed.
[34:44] Customer: Although this option has some limitations, because not all extensions are supported.
[34:49] Customer: The third option is to use some other code editors, like CodeMirror or something else, with plugins for debugging specifically, and for integrating with language server.
[35:10] Customer: Regarding the constraints about the code size for classes, the resulting problems or programs should be self-contained.
[35:28] Customer: So the student should be able to run that program, like inspect it in some ways, and the harness should be able to run it also.
[35:44] Customer: And probably it would be nice if it's possible for a student to copy all the generated code and run locally if they really want to, outside of our environment.
[35:58] Customer: So therefore, the example should be self-contained.
[36:03] Magel0n: Unfortunately, we need to recreate the Zoom meeting because, well, it's Zoom and it has been 40 minutes.
[36:10] Magel0n: We have three more questions and we'll reconnect for them, okay?
[36:17] Customer: Okay, I will connect too
[38:25] Magel0n: Yeah, I think we can proceed.
[38:28] Magel0n: So, if you could only do one thing well in our first version, which would you choose?
[38:40] Magel0n: Generated exercises for a chosen category, debugging in the user's own IDE, or a public gallery?
[39:00] Customer: I think... What do you mean by debugging in your own IDE?
[39:09] Magel0n: Well, the implementation of sending it to the IDE, like either downloading it and sending or copying the contents and sending.
[39:20] Customer: Okay, I think I will prefer this, debugging in your IDE somehow.
[39:32] Magel0n: Could you expand as to why?
[39:37] Customer: Yes, because it's like the most technically risky part, I guess.
[39:47] Customer: Like whether we can implement such a thing that it works more or less conveniently for a user.
[39:55] Customer: Whether we can even connect to a VM from the user's VS Code, or from the browser.
[40:03] Magel0n: And what would you rank second then?
[40:14] Customer: The other options were generating generated problems and...
[40:25] Magel0n: Public gallery.
[40:26] Customer: Yeah, public gallery.
[40:29] Customer: I think the generating exercises will be another important thing because we need to tweak the prompts to produce produce good exercises and it's also important to think how the setup will look like for an exercise, what the code layout will be, where the tools will be stored on a VM or in a container and so on.
[41:08] Customer: What will be shared between sessions, maybe some environment parts.
[41:16] Magel0n: Okay.
[41:19] Magel0n: So another question.
[41:22] Magel0n: What could we remove from the proposed direction?
[41:25] Magel0n: Maybe you can see something that is not that valuable.
[41:31] Customer: Sorry, remove from what?
[41:33] Magel0n: From the proposed direction.
[41:38] Customer: What can we consider the proposed direction?
[41:44] Magel0n: Well, us creating this system with the...
[41:50] Magel0n: Well, generating exercises, debugging the IDE, public gallery, creating the site for it, and...
[41:58] Magel0n: Using the keys and whatnot. Uh-huh.
[42:05] Customer: And what can we remove from this system?
[42:09] Magel0n: Well, if there is anything.
[42:17] Customer: I'm greedy, so I'm not willing to remove anything right now.
[42:21] Customer: But we will definitely discuss the scope in some of the next meetings.
[42:28] Magel0n: Okay.
[42:33] Magel0n: Would a single language, for example, Python, first version, be acceptable?
[42:40] Magel0n: Or do we need to support multi-language from the start?
[42:48] Customer: Single language for a prototype is okay.
[42:55] Customer: But the MVP, what you submit at the end of the course, should support several languages.
[43:02] Customer: Which of them we can decide later, but like...
[43:07] Customer: Probably this will be some mainstream languages like Python, Glow TypeScript, I don't know, maybe Java or Scala.
[43:25] Customer: The system should be designed in a way to support several languages.
[43:25] Magel0n: Okay, just in case, is there anyone else who knows about this problem differently from you so that we could speak with them?
[43:49] Customer: I think I don't know anyone who is thinking exactly about this problem.
[43:57] Customer: Maybe you can talk to some people administering the platforms like LeadCode or Codeforces or some participants, like active participants of those platforms, like contest creators.
[44:16] Customer: Maybe they have some thoughts about how to teach debugging to people.
[44:30] Magel0n: Well, in that case, our next step is, other than to continue with creating the report and whatnot, is to create the prototype and continue with the course.
[44:45] Magel0n: So, I believe... Does my team have anything else to say?
[44:57] Magel0n: Well, they are writing to me, but probably not.
[45:05] Magel0n: Well, do you have anything extra you wanted to add?
[44:10] Customer: Not yet.
[44:13] Customer: I'll be eagerly waiting for your prototype.
[45:19] Magel0n: Very well.
[45:21] Magel0n: In that case, I believe we are finished.
[45:24] Customer: Okay.
[45:26] Customer: Thank you for this kickoff.
[45:33] Magel0n: Well, thank you for coming and telling us so much about the ideas.
[45:41] Magel0n: All righty then, Goodbye.
[45:45] Customer: Yeah, have a nice evening, goodbye.
[45:47] Magel0n: You too.