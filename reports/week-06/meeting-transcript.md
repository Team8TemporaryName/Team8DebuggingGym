# Week 6 customer Sprint Review transcript

**Date:** 2026-11-09
**Participants:** Magel0n, Customer, Tedor49, NikitaRUniverse, Doosuur14

The permissions for recording, public sanitized-transcript publication, and private instructor sharing were all granted before recording began. The permission exchange is not part of this transcript.

Timestamps are retained from the source transcription; a small number of labels are out of sequence and are preserved rather than guessed.

[00:00:00] Magel0n: All right.
[00:00:10] Tedor49: Okay, hello, let me share my screen.
[00:00:10] Tedor49: I'm sorry, I won't be able to show you it running on a university VM since [redacted].
[00:00:10] Tedor49: So I think we can do with just showing you the new functionality we have implemented.
[00:00:10] Tedor49: So, first of all, we have implemented, well, saved exercises on the server.
[00:00:10] Tedor49: And, well, a learner can press a link and go to the exercise.
[00:00:10] Tedor49: So, then, just as we did it earlier, we can solve it and run the tests.
[00:00:10] Tedor49: both locally and on the server.
[00:00:10] Tedor49: Oh yeah, I need to save it actually for it to run.
[00:00:00] Magel0n: Yes.
[00:01:25] Tedor49: Yes, we fixed...
[00:01:25] Tedor49: Can you repeat your question?
[00:01:31] Customer: What did you save to run the...
[00:01:34] Tedor49: The file where I was solving the exercise.
[00:01:41] Customer: Okay, got it.
[00:01:48] Tedor49: So is there an autosave?
[00:01:48] Tedor49: Not right now.
[00:01:54] Customer: Is there a specific reason for this?
[00:01:59] Tedor49: No, there isn't.
[00:01:59] Tedor49: So I think we can add that.
[00:02:10] Customer: I agree.
[00:02:10] Customer: If there is no automatic submission on file save, then I think it's okay to add after save.
[00:02:10] Customer: And also we discussed after commits.
[00:02:10] Customer: they are like similar things like after saves Okay, let's proceed.
[00:02:39] Tedor49: Okay, let's proceed.
[00:02:39] Tedor49: So what we have added is we have added a separate access for the teacher.
[00:02:39] Tedor49: So you can enter a key right here and you can log in and you have a separate interface where you can actually will create exercises.
[00:02:39] Tedor49: so here we can enter some prompt for the exercise or maybe you have some suggestion but i can enter one myself yeah please enter one okay let's just do it something like okay here so right now it is generating and in a little bit of time we should see it appear in the exercise list so did you click generate and store yes i think maybe i did oh yes here it appeared now we have this exercise size which we can once again run some tests locally and fix it and we'll run the same tests and save it and run it simply and as you can see when we successfully solved it on the server and not locally a check mark appeared next to the exercise name which is stored per user but right now there is no well separate users so these are all just one user okay and so
[00:05:10] Tedor49: I think this is mostly it and another thing is well if you click exercise which you already have the files of it prompts you to if you want to re-download the files or not so if you have any changes for example you've already solved the exercise and you just want to look at the solution then you can then you cannot delete the whole directory and if you want to redo the exercise then you can download it again you can see
[00:06:05] Customer: The user can see their solution?
[00:06:07] Tedor49: Yes.
[00:06:13] Customer: Okay.
[00:06:13] Customer: Could you demonstrate like deleting a directory and downloading a nexus solution?
[00:06:32] Tedor49: Hmm oh you meant like that oh no it does not download the solution from the server it allows the user to keep their own files intact or download the exercise again uh don't quite get it so the the user
[00:06:54] Customer: User got an exercise from the server.
[00:06:54] Customer: I mean, in this case, they generated an exercise as a teacher, I guess.
[00:06:54] Customer: And they uploaded it to the server, right?
[00:06:54] Customer: Yes.
[00:06:54] Customer: Okay.
[00:06:54] Customer: And then if they delete this exercise on their machine, Then can they download from the server what was uploaded there before?
[00:07:35] Tedor49: Oh, yes.
[00:07:35] Tedor49: I think I should actually close VS Code so I can actually delete them.
[00:07:35] Tedor49: Okay.
[00:07:35] Tedor49: Let me share my screen again.
[00:07:35] Tedor49: Here, as you can see, all the exercises don't exist and this folder is pretty empty.
[00:07:35] Tedor49: So then we can go and download this exercise from the server again.
[00:07:35] Tedor49: Which one?
[00:07:35] Tedor49: How did you download it?
[00:07:35] Tedor49: I just pressed the button that displayed the exercises that are on the server.
[00:08:32] Customer: So all of these exercises they are the ones on the server if you press the exercise title it downloads its files from the show yes okay okay i also see the button like Yeah, this one.
[00:08:32] Customer: What does it do?
[00:08:58] Tedor49: Yeah, it refreshes the exercise list.
[00:09:05] Customer: Which state does it use?
[00:09:05] Customer: Like local state or server?
[00:09:09] Tedor49: It uses the state on the server.
[00:09:13] Customer: Okay.
[00:09:13] Customer: So how to delete an exercise on the server?
[00:09:29] Tedor49: Is it possible?
[00:09:29] Tedor49: Right now, no, it's not possible.
[00:09:33] Customer: I just imagine a situation when the teacher created a contest for students, then decided to create another one.
[00:09:33] Customer: Maybe they just copy the previous one and delete some exercises, like a simpler one, for example, and add some others.
[00:09:33] Customer: So that's why I was asking.
[00:10:05] Tedor49: Okay.
[00:10:05] Tedor49: we could implement that but but I also think that deleting stuff is generally I think not not a good idea since people can delete stuff accidentally so So maybe the button shouldn't be very visible, but the situation you described, I think deleting the exercise from the server would be useful then.
[00:11:03] Customer: Okay.
[00:11:03] Customer: I think I should reconnect.
[00:11:03] Customer: Just give me a moment.
[00:11:03] Customer: OK.
[00:11:03] Customer: Sorry, so we have like I wrote up this context, a contest thing, but I think we're.
[00:12:14] Tedor49: So can you.
[00:12:14] Tedor49: Oh.
[00:12:14] Tedor49: Can you repeat, please?
[00:12:14] Tedor49: You are breaking up.
[00:12:17] Customer: Sure.
[00:12:17] Customer: So I mentioned a contest that the teacher creates and then copies it, creates another one.
[00:12:17] Customer: But I think we did not discuss this approach.
[00:12:17] Customer: I think we only discussed creating an exercise and assigning it to groups of students or to particular students.
[00:12:55] Tedor49: Did we?
[00:12:55] Tedor49: Yes, we did not discuss creating contests.
[00:00:00] Magel0n: Only maybe some groups of exercises.
[00:13:09] Customer: Okay.
[00:13:09] Customer: But I wonder if this might be useful.
[00:13:09] Customer: Like creating or selecting several exercises for a lab, for example.
[00:13:09] Customer: How do we assign them to the group?
[00:13:09] Customer: Do we assign each individual exercise to a group of students or do we somehow group the exercises and then assign the group of exercises to like a student group like problem set i think we can implement both since uh
[00:14:11] Tedor49: Since both of these modes of operation can be useful, in my opinion.
[00:14:11] Tedor49: And I don't think it will be particularly difficult if we don't make groups of exercises very separate things.
[00:14:37] Customer: Okay, great.
[00:14:37] Customer: So please experiment on whether it works.
[00:14:37] Customer: Maybe you can somehow fuse those two scenarios and make something even more convenient.
[00:15:03] Tedor49: Okay.
[00:15:04] Customer: Okay.
[00:15:04] Customer: Maybe there can be a contest with only one exercise.
[00:15:04] Customer: This will cover the scenario when one exercise is assigned to a group of students.
[00:15:04] Customer: So maybe just assigning a problem set is enough.
[00:15:04] Customer: I don't know how to call it, like exercise set.
[00:15:38] Tedor49: Personally, yes, we can call it an exercise set.
[00:15:38] Tedor49: I was thinking of more of a folder like structure where you can create folders and folders inside folders and assignments inside folders, and you can assign any one of them to any group of students.
[00:16:08] Customer: Uh-huh okay and what if i want to share an exercise between those folders like i have two groups i give like two same exercises to those groups and two different ones
[00:16:33] Tedor49: Each group receives four exercises i think both of them should well receive all of the exercises that they were assigned and well we can store not it's not like literal folders but we can store just links to the exercises so that the same exercise can be in both folders and they are a little bit separated like Oh.
[00:16:33] Tedor49: This is the shit.
[00:18:38] Customer: I wonder if there might be some problems for the tooling working with links to exercise folders.
[00:18:38] Customer: If we literally use symlinks, extensions recognize the files in that folder as normal files.
[00:18:38] Customer: And also another consideration is if I'm editing an exercise as a teacher and we use symlinks, to not duplicate files, then all versions of this exercise will be edited, which I may want to not have.
[00:19:57] Tedor49: OK.
[00:19:57] Tedor49: I don't think it will be literal symlinks I think it will more just be and it will not be a literal folder system so and I think it will be mostly well simulated and you told us before that one of the scenarios you imagine is well creating a copy of a contest I think well that could also apply to well exercises but I think if a teacher wants to edit an exercise and make it different just in that one folder and the exercises in several folders right now, I think they should be able to copy it.
[00:19:57] Tedor49: I don't think by default it should segregate.
[00:19:57] Tedor49: this exercise from the rest of its links to it what do you think?
[00:21:38] Customer: Okay, I agree.
[00:21:38] Customer: I think we can't decide for the teacher whether they want to edit this particular exercise or all versions of it in other exercise sets.
[00:21:38] Customer: So I think we can let the teacher choose what they want to do in our extension panel.
[00:21:38] Customer: Maybe they click an exercise, and then they can choose edit, only this one, or edit everywhere, something like this.
[00:21:38] Customer: And then they can proceed to editing the files.
[00:22:38] Tedor49: I think it would...
[00:22:38] Tedor49: I don't know when would be the best time to make this segregation but I think we should also consider making it at the end so the teacher can just well download that exercise and then they can edit it and then they can well click the upload button so so what would you think is the best approach because i'm not really sure about making the teacher choose whether to edit it locally or globally when they open the exercise okay editing can only happen in this code because like
[00:24:00] Customer: Well, we don't provide any other editor.
[00:24:00] Customer: But like deciding what to do with an exercise.
[00:24:00] Customer: Yes, it should also happen in VS Code.
[00:24:00] Customer: But like globally or locally, should we propagate local changes to the server?
[00:24:00] Customer: I think it should be up to the teacher.
[00:24:00] Customer: I brought up the case when the teacher has several exercise sets locally, and they want to edit an exercise that belongs to all of those exercise sets.
[00:24:00] Customer: And then they edit one of them, one of the files, one of the versions, and then they then they like click sync for example or i don't know like update everywhere and like all either all local exercises are updated like all local versions or the version on the server uh There is a public gallery where the teacher downloads an exercise from.
[00:24:00] Customer: So if they decide to edit an exercise, then a new exercise should be created.
[00:24:00] Customer: I mean, if...
[00:24:00] Customer: Yeah, I think a new one should be created even if...
[00:24:00] Customer: Or...
[00:24:00] Customer: unless the teacher is the author of the original exercise in the public gallery like in this case they have permission to edit this exercise in the public gallery otherwise not okay
[00:26:10] Customer: And yeah, in students with code extensions, it would be nice to show like some message that an exercise was updated on the server.
[00:26:10] Customer: Like teacher pushed some changes to the server.
[00:26:10] Customer: Everyone should receive them.
[00:26:40] Tedor49: Do you think the student should receive the updates automatically or they should re-download the exercise manually?
[00:26:56] Customer: The problem is that the student may have made some changes to the files of this exercise.
[00:26:56] Customer: We need to somehow reconciliate them with the version of the server.
[00:26:56] Customer: Maybe like via local rebase or I don't know, like let the students somehow transfer those changes to the server version.
[00:26:56] Customer: Not sure what what the best approach is, honestly.
[00:26:56] Customer: But I think automation may work, but it might cause some merge conflicts or something like this that should be resolved by the student.
[00:26:56] Customer: And I'm not sure how to implement this properly.
[00:26:56] Customer: So automatic version may not be very convenient or maybe hard to implement.
[00:26:56] Customer: So I would rely on manual version.
[00:28:22] Tedor49: Okay.
[00:28:22] Tedor49: So we will implement like an icon that shows if the exercise was changed on the server.
[00:28:34] Customer: Mm-hmm.
[00:28:34] Customer: Yeah.
[00:28:34] Customer: And then, okay, what happens then?
[00:28:34] Customer: Okay, maybe the student should be able to download these new files.
[00:28:34] Customer: And they're like previous changes.
[00:28:34] Customer: should be moved to some like another folder maybe which will not will not be the source of truth for the student submission anymore uh i mean they they worked on an exercise in a folder abc then The teacher updated the exercise on the server.
[00:28:34] Customer: The student downloads this updated version into the folder DEF.
[00:28:34] Customer: And this DEF folder becomes the source of truth for the student's submission.
[00:28:34] Customer: When they click submit, then this DEF is sent to the server, not ABC.
[00:28:34] Customer: and from abc they should be able to transfer the changes to the idf i don't know maybe we should instruct them to compare files i think as uh
[00:30:20] Tedor49: We are using Git for tracking changes that the student has made to the files.
[00:30:20] Tedor49: We can try to move the changes using Git, and then if that doesn't succeed automatically, we can urge the student to resolve the conflicts.
[00:30:48] Customer: Okay.
[00:30:48] Customer: Okay, I wonder...
[00:30:48] Customer: if students will be prepared enough to resolve the conflicts, but they will have to resolve those conflicts anyway.
[00:30:48] Customer: So maybe it's an okay idea.
[00:30:48] Customer: So yeah, if we're using your approach, maybe we can create a new branch that replaces like the old exercise version with a new one.
[00:30:48] Customer: And then start the merge.
[00:30:48] Customer: And then ask a student to resolve conflicts.
[00:30:48] Customer: What do you think?
[00:30:48] Customer: Or do you have some other approach in mind?
[00:31:38] Tedor49: I was thinking more of saving the diff between the exercise on the student's computer and the old version and then trying to then saving the old version to some other directory maybe with the same id but just tagged with old and And while trying to apply this change, this diff that we have saved to the new folder.
[00:31:38] Tedor49: So like Apache?
[00:32:24] Customer: Yes.
[00:32:24] Customer: Okay.
[00:32:24] Customer: Okay.
[00:32:24] Customer: I'm honestly not sure if it will work with given arbitrary code changes between the old exercise version and the new one.
[00:32:24] Customer: As far as I know, the patch relies on line numbers, which may be different.
[00:32:24] Customer: for the new exercise version.
[00:32:24] Customer: So you may not be able to apply a patch.
[00:32:24] Customer: Like you can have a diff between like this solution and the original alt exercise.
[00:32:24] Customer: But then how do you apply this diff in this patch?
[00:33:38] Tedor49: Well, right now I am aware of git stash, which in my experience will solve this exact problem where I need to save some changes and then move them to some other place.
[00:33:38] Tedor49: so I was thinking of well looking at alternatives and using it and also about arbitrary changes I think that this process of migration from the old version of the exercise to the new version of the exercise, I don't think it should trigger automatically.
[00:33:38] Tedor49: I think it should be manually triggered by the user so that if the change is very big, they can either not trigger it or see that It's too much work to integrate the patch and revert it.
[00:33:38] Tedor49: And then they can just resolve the exercise.
[00:33:38] Tedor49: Well, move their solution manually.
[00:33:38] Tedor49: Because I think this is always going to be an option that is sometimes required.
[00:35:29] Customer: Okay, I agree.
[00:35:29] Customer: So, in any case, okay, it's nice that you mentioned git stash.
[00:35:29] Customer: Yeah.
[00:35:29] Customer: It will probably do the work.
[00:35:29] Customer: I think it's important to somehow preserve the students' changes that they made before, to not lose them in any case.
[00:35:29] Customer: So we need some solution for this.
[00:35:29] Customer: Well, git stash stores them in the git history, as far as I know.
[00:35:29] Customer: of course somewhere in git oh yes somewhere in git so you don't lose it like after applying yes yes you don't lose it there's just a long catalog of stashes okay this might indeed work uh All right.
[00:35:29] Customer: And then we should rely on some VS Code extensions to resolve conflicts, I guess.
[00:35:29] Customer: So students should have something installed in VS Code, either some built-in thing or GitLens or something simpler.
[00:35:29] Customer: Not sure what to recommend.
[00:37:07] Tedor49: OK, we will see.
[00:37:12] Customer: Okay.
[00:37:12] Customer: Okay.
[00:37:12] Customer: So we somehow can update files on the student's machine.
[00:42:36] Magel0n: That's nice.
[00:37:35] Customer: And we can upload files like as a teacher to the server.
[00:37:35] Customer: Okay.
[00:37:35] Customer: And we We have permissions like the teacher can update their own files, like their own exercises, but not others exercises.
[00:37:35] Customer: Yeah, basically, if they download someone else's exercise from the public gallery and then edit it locally, then they can only upload their own version and become their author.
[00:37:35] Customer: They can't.
[00:37:35] Customer: Edit the original version.
[00:37:35] Customer: Okay.
[00:37:35] Customer: Okay.
[00:37:35] Customer: So you have a nice extension now.
[00:37:35] Customer: And they see here teacher login.
[00:37:35] Customer: Do students also see this teacher login?
[00:38:41] Tedor49: Right now right now there is a separate button for teacher login but so you can well enter the access key and get the access to the teacher panel but i think in the future version where in the next version where we add accounts we will just have before you can see everything a login form and that will differentiate between teacher and student and so this button will not exist for the student oh i agree this is this sounds like a good approach i'm not sure what they don't need right now
[00:39:28] Customer: Okay, exercises on the server.
[00:39:28] Customer: So how do they run programs right now?
[00:39:28] Customer: Do they run them in a container, like students or teachers?
[00:39:45] Tedor49: Right now they run on the computer themselves, itself.
[00:39:50] Customer: Okay.
[00:39:50] Customer: My biggest concern is that like, they run agent generated code on their machine without any sandboxing.
[00:39:50] Customer: This my like, do some harm to this machine and therefore I suggested that like even locally they run in a container or in another kind of sandbox what do you think is it doable
[00:40:36] Tedor49: I think it is it will be hard but i think it will be doable but i but i think uh it won't be doable soon because i think we should implement the other features first and this is not a very big priority because the exercises should be double checked by the teacher okay
[00:41:20] Customer: Okay, another concern is that code in the exercises may intentionally edit some files.
[00:41:20] Customer: Like read some files, write some files where it may be like not here, but in home or in another directory outside of this one that stores all of the exercises.
[00:41:20] Customer: So in this case, some sandboxing would also be very useful to prevent changes on the machine of a student or a teacher.
[00:41:20] Customer: So, okay.
[00:41:20] Customer: I would suggest to like not push it to the very end of the project because this unboxing is a useful thing.
[00:41:20] Customer: At least please research like which options exist or try it with containers.
[00:42:36] Magel0n: Okay.
[00:42:36] Magel0n: i see another problem in it since if we try to add containers and whatnot and adding it all onto it uh then we may arise with the where the creation of all of the sister or the setup for the student gets overcrowded and just much harder compared to the original idea that well the teachers are supposed to check what they are pushing as their code, as we consider them as trusted users.
[00:43:09] Customer: Yeah, I see this concern.
[00:43:09] Customer: Okay, but But we want to make sure that the exercise runs the same way on each student's machine.
[00:43:09] Customer: And so the containers are a way to achieve reproducibility.
[00:43:09] Customer: Another one is to require everyone to use Linux and Nixos or another virtual machine.
[00:43:09] Customer: approach.
[00:43:09] Customer: So like, of course, the code can be trusted, because the teacher authored it, but it may include, like modifying some files intentionally, like, just for the purpose of the exercise.
[00:43:09] Customer: And so it would be nice to sandbox it anyway.
[00:44:23] Magel0n: We will see what we can do, but on the contrary, I could see an interesting trick of an exercise where the teacher is interested in seeing if the students actually read the exercise.
[00:44:23] Magel0n: For example, he just has a counter that is written outside of where they are right now, so the student should see and realize why something is changing.
[00:44:49] Customer: I don't quite get this point.
[00:44:49] Customer: What do you mean?
[00:44:56] Magel0n: Which counter?
[00:44:56] Magel0n: Is this an undesired behavior that this is not that sandboxed?
[00:44:56] Magel0n: Or should we still try to leave some options for it available?
[00:44:56] Magel0n: I don't know.
[00:44:56] Magel0n: Maybe my colleague has some other way to phrase it.
[00:45:18] Customer: Okay, waiting for his opinion.
[00:45:18] Customer: but if peder is talking i can't hear him uh no i was not talking
[00:45:39] Tedor49: So the question is, is modifying the files outside of the exercise directory?
[00:45:39] Tedor49: I understood that it can be a part of exercise, so it should be supported, but since it could mess with the user system, it should be sandboxed.
[00:46:02] Customer: I support.
[00:46:02] Customer: Okay.
[00:46:02] Customer: And we're talking about computer science students kind of right now.
[00:46:02] Customer: So they may have some problems with Docker setup, but...
[00:46:02] Customer: Overall, it shouldn't be a very big deal to run a container.
[00:46:02] Customer: Moreover, we can run containers for them.
[00:46:02] Customer: They click an exercise, they click, I don't know, start a container or solve locally.
[00:46:02] Customer: Oh, no.
[00:46:02] Customer: It's a tautology.
[00:46:02] Customer: They always solve locally.
[00:46:02] Customer: Start solving or start...
[00:46:02] Customer: I don't know which one is more intuitive.
[00:46:02] Customer: And then VS Code connects to that container and they run their commands in that sandbox.
[00:46:02] Customer: So it might not be very hard to shut off and switch between exercises.
[00:46:02] Customer: Okay, we can try to implement that.
[00:46:02] Customer: Nice, thank you.
[00:46:02] Customer: Also, It would be nice to let them refresh the sandbox, start it anew, if they mess up something inside it.
[00:46:02] Customer: Yeah, and then they will be equipped for local solving while they're waiting for the server.
[00:46:02] Customer: to submit their exercises.
[00:46:02] Customer: I mean, the server might be busy sometimes and students should be able to check locally while they're waiting for the server.
[00:46:02] Customer: Do that safely.
[00:48:43] Tedor49: Okay.
[00:48:54] Customer: All right.
[00:48:54] Customer: So right now they have this directory with exercises and they're all in Python, right?
[00:48:54] Customer: Yes.
[00:48:54] Customer: Okay.
[00:48:54] Customer: Where do you store dependencies, Python dependencies?
[00:49:22] Tedor49: Right now, nowhere.
[00:49:26] Customer: Where can they be stored?
[00:49:26] Customer: In every directory?
[00:49:34] Tedor49: I believe we discussed this previously and we settled on the solution that we can store dependencies for each exercise but we can also try to use a package manager like uv so the dependencies can be cached
[00:49:59] Customer: Okay.
[00:49:59] Customer: And here we are talking.
[00:49:59] Customer: Why do we need the dependencies?
[00:49:59] Customer: Because we want to see types in the code and run some code and so on.
[00:49:59] Customer: If we use sandboxing, we can connect with code to the sandbox.
[00:49:59] Customer: and run everything there inside the sandbox.
[00:49:59] Customer: So the sandbox can store the actual dependencies.
[00:49:59] Customer: Maybe there is a way to share the dependencies.
[00:49:59] Customer: Like if this are Docker containers, maybe there can be like a base image that will be shared.
[00:49:59] Customer: between containers.
[00:49:59] Customer: And yeah, so the UV way could also work inside the sandbox, I guess.
[00:49:59] Customer: For now, it's okay that it works outside of it.
[00:49:59] Customer: And that scripts run in the bare terminal.
[00:49:59] Customer: But later, it would be better to run everything inside the sandbox.
[00:49:59] Customer: Like for consistency, at least.
[00:49:59] Customer: Okay.
[00:49:59] Customer: Assume you implemented this thing, then when they start working on an exercise, I guess another VS Code window should open, which is connected to the sandbox.
[00:49:59] Customer: And then, yeah, like every terminal that they open in this VS Code will open in the sandbox.
[00:49:59] Customer: All extensions can either be installed in that sandbox.
[00:49:59] Customer: Not sure if that's right.
[00:49:59] Customer: Or, oh no.
[00:49:59] Customer: I think extensions will be installed in the VS Code.
[00:52:33] Customer: But I think extensions are stored somewhere on the machine and installed into VS Code at some point.
[00:52:33] Customer: Not sure when is the right moment to install them in this newly opened VS Code window, second VS Code window that is connected to the sandbox.
[00:52:33] Customer: but they should be available there.
[00:53:17] Tedor49: Understood.
[00:53:30] Customer: As for VS Code settings, So we have like VS code for each exercise in this case.
[00:53:30] Customer: And then we should have like separate settings for each VS code perhaps like because Because some exercises may require some Golang-specific settings, some other Python-specific settings.
[00:53:30] Customer: And so there should be a .vscode-settings.jp file somewhere near the exercise directory, I assume.
[00:53:30] Customer: And I'm not sure whether it should be provided by the teacher or generated dynamically by our extension or edited by our extension.
[00:53:30] Customer: I'm not sure if we should abandon the current mode where students can run commands in the terminal.
[00:53:30] Customer: Maybe for some simpler exercises, completely verified, which can do any harm to the system.
[00:53:30] Customer: This might be a more convenient way.
[00:53:30] Customer: For some hardcore exercises, it needs to be started.
[00:53:30] Customer: But anyway, even if we somehow share the dependencies, like I said, this is the code that you show now.
[00:53:30] Customer: And the dependencies are stored in the corresponding exercise directories.
[00:53:30] Customer: We need to somehow tell extensions which dependencies to use.
[00:53:30] Customer: Like we can't have a single pyproject.toml, I guess, in the root because All exercises may need different package versions.
[00:56:54] Customer: And so you will not be able to create a single log file that satisfies all of the bounds.
[00:56:54] Customer: So we should either open a new VS code in each exercise directory, And it will see, like, write dependencies, write files, like, write by project or, yeah.
[00:56:54] Customer: I think there is no other way.
[00:57:19] Tedor49: I was thinking for Python we could maybe use, well, virtual environments.
[00:57:19] Tedor49: Since if I remember correctly, they are designed for this purpose, exactly.
[00:57:35] Customer: Okay, yeah.
[00:57:35] Customer: The second way, yeah, is to use a virtual environment.
[00:57:35] Customer: I mean, in the first approach, it's also used and it's stored inside the exercise directory.
[00:57:35] Customer: Yeah, and we should somehow tell the Python extension which environment to use in this case.
[00:57:35] Customer: When they choose an exercise that involves PyTorch, then the Python extension should switch to that environment.
[00:57:35] Customer: Sorry for interrupting.
[00:58:15] Tedor49: No problem.
[00:58:15] Tedor49: I didn't have much else to say.
[00:58:15] Tedor49: well I think that probably the virtual environment should be alongside the exercise well stored on the server and probably we want so that probably we also want so that a teacher can edit it
[00:58:49] Customer: So they can tweak package versions and whatnot okay agree yeah by the way it would be convenient for a teacher to see to get some scaffolding for exercises like they select the exercise language like Golang or Python.
[00:58:49] Customer: And then like several files appear.
[00:58:49] Customer: The exercise itself, like with `__main__` or something like this.
[00:58:49] Customer: The tests, the harness file, like the private harness file, the public harness file, and maybe this, pyproject.toml file for exercise-specific settings.
[01:00:09] Tedor49: Yes, I think that will work.
[01:00:16] Customer: And a similar thing Should there be a docker file by the way?
[01:00:16] Customer: I don't know which approach will work for sandboxing.
[01:00:16] Customer: If it's via containers, then...
[01:00:16] Customer: maybe we should expose the docker file as well that will be used to build containers for this for checking this exercise on the server or locally by students so that the teacher can tweak it like fix something yeah I agree that we should probably expose the docker file or
[01:01:08] Tedor49: And I think we can pretty much expose everything to the teacher and almost everything to the student yeah we should not expose the private harness only and is that it?
[01:01:08] Tedor49: i think maybe if at some point we want the teacher to provide a solution for the task then we should also not expose that but other than that no i don't think there is anything that should not be exposed okay okay um
[01:02:11] Customer: All right.
[01:02:11] Customer: I have a question regarding generating new exercises.
[01:02:11] Customer: So how does it work today?
[01:02:11] Customer: Do you generate the correct version?
[01:02:11] Customer: Does it exist?
[01:02:11] Customer: Or do you generate a buggy version first?
[01:02:42] Tedor49: We generate a buggy version and we will generate the harness and right now no correct version is generated but I was also thinking that well it should be yeah there should be like an oracle kind of the ground truth
[01:03:12] Customer: And like harness should be tweaked against this version okay okay so the this unboxing problem yeah we discussed There is a problem that the student can still manipulate the test runner on the server, but I'm not sure how to prevent this.
[01:03:12] Customer: I think codeforces uses only standard input, standard output.
[01:03:12] Customer: And so like the program cannot interact directly with the test panel.
[01:03:12] Customer: But here we assume run the test runner like after importing the student's solution.
[01:03:12] Customer: yes kind of and so yeah i'm not sure what to do about this like should we limit the the range of exercises or should we trust our students well i don't think we should trust our students ever well yes But like if you don't trust them, then solutions might be very complicated.
[01:05:16] Tedor49: Yes.
[01:05:23] Customer: There was a suggestion from another team, like let's use an agent to check every submission.
[01:05:41] Tedor49: Whether it contains some malicious code but I think it will not discover all cases Python has a lot of ways of circumventing anything starting from just exec and deval and ending with the globals
[01:06:17] Customer: Dictionary.
[01:06:17] Customer: Yeah.
[01:06:17] Customer: So I don't know.
[01:06:17] Customer: Honestly, like my initial thought was to limit the the range of places that can be edited in a program.
[01:06:17] Customer: Since we have a ground truth, like the correctly solved exercise, and we have the buggy version, we can create a div and basically not allow editing other lines except for lines that differ.
[01:07:00] Tedor49: I don't think that is going to work because well you can just write whatever in those several lines and they will still execute as code if they are yes if they are anywhere and imports work anywhere right yeah yeah and also you can just use this import
[01:07:19] Customer: Which is the function so you can also pass strings to it so yeah okay this is a pretty hard question that might kill the project idea there is an approach like just parse an IFT of the program and then identify some keywords, import, ban them where they don't belong.
[01:08:16] Tedor49: Yes in fact in fact for my thesis I have done something similar to this and also But the difference here is that we do want some select functionality, which might be abused, like opening files.
[01:08:51] Customer: Right.
[01:08:55] Tedor49: So unless we unless we heavily reduce the scope of what we want to do and maybe for file specifically we can try to sandbox it and restrict the files that can open then it is maybe achievable But I don't think it would be achievable soon at all.
[01:09:30] Customer: Yeah.
[01:09:30] Customer: Actually, I think we can't trust students.
[01:09:30] Customer: Like, they run something, and then they submit, and it stays on the server.
[01:09:30] Customer: They just can't remove it.
[01:09:30] Customer: And then we just make a single pass with an agent after they submit everything, after the deadline.
[01:09:30] Customer: And we can see which submissions have such bypasses, workarounds, hacks, and so on.
[01:09:30] Customer: And then we can just report and do, yeah.
[01:10:21] Magel0n: May I ask you, Aren't we expecting the teachers to still check the submissions outright? 250 students?
[01:10:36] Customer: Good point.
[01:10:36] Customer: Yeah, we have TAs, but I think an agent would do a better job, honestly.
[01:10:36] Customer: I can't more consistently.
[01:10:36] Customer: okay so for right now we can just continue and implement just that the work is tracked on the git repository yes yes and on the server as well like students can delete their successful submissions at least or maybe any submission from the server like if they do some harm to the server then we can see that what caused this harm and punish them okay okay I think that's it from my side.
[01:10:36] Customer: Do you have something else to discuss?
[01:12:07] Tedor49: I don't think we have.
[01:12:07] Tedor49: I will pass the word on to Magel0n.
[01:12:19] Magel0n: I must admit that this was a rather lengthy talk.
[01:12:19] Magel0n: Let's try to complete what I have to ask you swiftly.
[01:12:19] Magel0n: Okay.
[01:12:19] Magel0n: So, the thresholds of success.
[01:12:19] Magel0n: Well, we've had four of them from the beginning of the project.
[01:12:19] Magel0n: I believe we've even discussed them with you when we first created them.
[01:12:19] Magel0n: But, well, it is time to check if we have completed them.
[01:12:19] Magel0n: So...
[01:12:19] Magel0n: Well, maybe not completed them, but achieved them to what degree?
[01:12:53] Customer: So, the first...
[01:12:53] Customer: Could you please show the text?
[01:12:53] Customer: What?
[01:12:53] Customer: Could you please show the text of this threshold of success?
[01:13:07] Magel0n: Well, that's the problem, as you could have seen my secondary monitor.
[01:13:07] Magel0n: The laptop is dead.
[01:13:07] Magel0n: Mm-hmm.
[01:13:07] Magel0n: So if you want me to, I can send you the link to the original Thresholds of Success.
[01:13:26] Customer: This might also work or maybe...
[01:13:26] Customer: Okay, I will be able to comment on it.
[01:13:33] Magel0n: Yeah, I think that should work.
[01:13:33] Magel0n: So you don't mind if I send it to Telegram, do you?
[01:13:33] Magel0n: Yep.
[01:13:33] Magel0n: So here are the Thresholds of Success.
[01:13:50] Customer: I will share my screen then.
[01:14:08] Magel0n: Excellent.
[01:14:11] Customer: Okay.
[01:14:11] Customer: Here I see threshold of success.
[01:14:19] Magel0n: Precisely well yeah i can see it clearly well i also have my own little version for myself because well i was supposed to talk with you uh-huh so uh for the first threshold of success regarding the core task being completable ends to end well we have been demonstrating the workflow several times now so would you consider this success criterion achieved or is there something significant that would you would consider core functionality um okay By the way, the original core functionality was, well, you can read it there, but it was about, you know, selecting a problem kind, generating an exercise, opening in VS Code, debugging it, receiving a verification result.
[01:15:23] Customer: I think it was a bit more complicated at the time.
[01:15:23] Customer: Like now I expect that the user does not need to read the setup.md.
[01:15:23] Customer: Debug it.
[01:15:23] Customer: Connect the ROM with code.
[01:15:23] Customer: Okay, I think it should be reformulated completely.
[01:15:23] Customer: Like what is the clean checkout?
[01:15:23] Customer: And where is the extension mentioned?
[01:15:23] Customer: And so on.
[01:15:23] Customer: Did something break?
[01:16:16] Magel0n: No, I can still hear you clearly.
[01:16:16] Magel0n: The problem is that, well, originally we weren't necessarily sure about the VS Code extension and whatnot.
[01:16:16] Magel0n: And the core idea itself was, well, abstract.
[01:16:16] Magel0n: To just have a problem kind, to have an exercise.
[01:16:16] Magel0n: to connect to it somehow to debug it and receive a result so perhaps we should pinpoint the elements or should we still keep it quite abstract okay i think you can just blade the measure like to
[01:17:06] Customer: To correspond to what we know now about the core task of a student.
[01:17:06] Customer: And also, so I think the core task itself should be extended, like it's not enough To generate an exercise and solve it locally.
[01:17:06] Customer: By the way, do we have a threshold of success about the public gallery and so on?
[01:17:49] Magel0n: I believe that we do not.
[01:17:49] Magel0n: We have one about the documentation availability.
[01:17:49] Magel0n: We have one about trustworthiness of the verification.
[01:17:49] Magel0n: We have one about the acceptance of the initial candidate probably was talking about it.
[01:17:49] Magel0n: And we were talking about the gallery wasn't fully necessary or something like that, was it not?
[01:17:49] Magel0n: Let me check.
[01:17:49] Magel0n: I have my notes here.
[01:17:49] Magel0n: well it seems like including our decisions we have let me check the decisions additionally but Seems to me that it is fine.
[01:19:16] Customer: The decision was taken.
[01:19:16] Customer: I mean, I don't mind if you keep this item and you like make it done or achieved.
[01:19:16] Customer: But I would suggest to add a new one about the extended core task, given that you now know more.
[01:19:45] Magel0n: I see.
[01:19:45] Magel0n: Very well.
[01:19:51] Customer: We shall add it.
[01:19:59] Magel0n: Regarding what you have said in Decision 005, we have started to focus more on the core ideas and what we can do regarding the AI and whatnot.
[01:19:59] Magel0n: So the multi-language and public gallery stories have been pushed to secondary perspectives.
[01:20:24] Customer: Yeah, I see.
[01:20:28] Magel0n: Hence why we have accepted the minimal useful product but well it is still open it's just to do yes
[01:20:41] Customer: I mean, this product will not be like really a product suitable for classrooms unless it has some way to transfer problems from teachers to students and letting students submit
[01:21:03] Magel0n: I see that the issue here is that, yes, we have mentioned that, and we have, as you've been discussing with my colleague, have been discussing ways of how to do it and whatnot, but we haven't picked one distinct solution that we would like to, and we didn't market in any of the TOSs.
[01:21:25] Customer: Mm-hmm.
[01:21:50] Magel0n: Besides, well, they weren't ever in the TOSs because, well, the TOSs were created to accept the minimal useful product and the combination of availability and whatnot.
[01:21:50] Magel0n: Well, that's why we're here because, well, we need to create new thresholds, proposals and whatnot.
[01:21:46] Customer: So I guess we can end that.
[01:21:51] Magel0n: Okay.
[01:21:51] Magel0n: Let me quickly go...
[01:21:51] Magel0n: What?
[01:21:54] Customer: If you'd like to discuss the exact formulation of the TOS goal, you can discuss it.
[01:22:04] Magel0n: Well, let's first finish up with what we originally had.
[01:22:04] Magel0n: You've said about the core task end-to-end.
[01:22:04] Magel0n: It should be expanded due to the knowledge that we have acquired.
[01:22:04] Magel0n: Regarding the trustworthiness of the exercise verification, I believe we have achieved it.
[01:22:31] Customer: Personally, I was quite unsure why it was much of a problem.
[01:22:31] Customer: generated exercise contains the intended defect and the learner's fix is judged by harness the learner cannot tamper with don't know this word tamper with mesh loss change falter yeah so right now we decided to drop this tamper with because we'll just store all the submissions and then check them.
[01:22:31] Customer: And then, yeah, this thing is achieved.
[01:22:31] Customer: We go in the same direction.
[01:23:45] Magel0n: We achieved this.
[01:23:45] Magel0n: Excellent.
[01:23:45] Magel0n: Customer reception of the initial candidate regarding TOS3.
[01:23:45] Magel0n: I believe that was, well, You did accept our minimally usable product.
[01:24:06] Customer: We just said what was next and we'll continue working on it.
[01:24:14] Magel0n: We're left out of the candidate.
[01:24:14] Magel0n: Yes, I guess it's done as well.
[01:24:14] Magel0n: And the last one is the documentation availability and whatnot about the documentation site being accessible, the GitHub pages.
[01:24:26] Customer: Can reach the product and its documentation without cloning the repository.
[01:24:26] Customer: Okay.
[01:24:26] Customer: Well, that is available.
[01:24:26] Customer: Let me just briefly check whether it's available now.
[01:24:26] Customer: I can send it to you.
[01:24:26] Customer: Okay.
[01:24:46] Magel0n: Or you can find it there.
[01:24:48] Customer: Yeah.
[01:24:48] Customer: Wonderful.
[01:24:48] Customer: Minimalistic.
[01:24:48] Customer: okay uh anyway it's it's it's achieved a moment Okay.
[01:24:48] Customer: So, yeah, I'll continue sharing the screen.
[01:25:47] Magel0n: Oh, very well.
[01:25:49] Customer: And it's documentation without running the repository.
[01:25:49] Customer: A learner can reach the product.
[01:25:49] Customer: Okay.
[01:25:49] Customer: Why did we need this?
[01:26:07] Magel0n: Oh, that's a difficult question.
[01:26:07] Magel0n: Do you need me to check it through all the decisions?
[01:26:16] Customer: I just see no associated decision.
[01:26:16] Customer: Therefore I wonder
[01:26:24] Magel0n: I believe that one of the ideas was that most of this should be available to be insinuated locally and whatnot.
[01:26:24] Magel0n: Hence why it was somewhat of a necessity for them to be able to read what they are actually putting on.
[01:26:55] Customer: Got it.
[01:12:07] Tedor49: Okay.
[01:12:07] Tedor49: Uh...
[01:26:55] Customer: Well, yes, but, like...
[01:27:02] Magel0n: Since then, we have changed it to be more about...
[01:27:02] Magel0n: What, what?
[01:27:07] Customer: We don't really expect students to, like, deploy it somehow, like, read the docs, read the...
[01:27:07] Customer: Oh...
[01:27:15] Magel0n: Well perhaps then we can simply change it to be not students but for example teachers if the original website is ever down they can hypothetically do it themselves um yes and it's just following the setup so it's not that hard we have another role i guess who is not a teacher ah or
[01:27:41] Customer: We didn't discuss this.
[01:27:41] Customer: Okay, there is some operator of the system, like an admin, who sets up teachers' accounts and students' accounts, I guess.
[01:27:41] Customer: And so this GitHub website And setup instructions in particular might be more of interest for this operator than for teachers.
[01:27:41] Customer: But nevertheless, the setup instructions should be accessible to everyone using this project.
[01:27:41] Customer: Maybe they become an operator at some point so i would suggest to just replace a learner with something more neutral like a product user product potential product operator an aspiring deployment enthusiast
[01:29:14] Magel0n: I don't know, like...
[01:29:14] Magel0n: Well, we'll figure it out.
[01:29:17] Customer: Yeah.
[01:29:19] Magel0n: Very well.
[01:29:22] Customer: Great.
[01:29:22] Customer: So, we should set some more relevant goals then.
[01:29:22] Customer: So, one of them is already set.
[01:29:22] Customer: Like, the learner can complete the end-to-end scenario.
[01:29:22] Customer: Another TOS goal...
[01:29:44] Magel0n: I would like to also have a proposal that will require discussion.
[01:29:44] Magel0n: Well, since our value propositions have learners receiving targeted debugging practices and improving their debugging skills, wouldn't it be good for us to have a focus metric that would be the amount of completed exercises per active learner per week?
[01:29:44] Magel0n: or something akin to that.
[01:29:44] Magel0n: Should we move towards that as, well, one of our tasks is to try and create more sizable metrics?
[01:29:44] Magel0n: Yeah.
[01:29:44] Magel0n: The obvious problem, like, the direction of it seems to be, well, the only possible direction because this is where we need to go for our value prepositions but that would require us to have some real student usage and some actual course usage then yeah i see and like if a course with 250 students uses this product
[01:30:58] Customer: You do get this like weekly students, like weekly submissions.
[01:30:58] Customer: You can achieve this metric that we said.
[01:30:58] Customer: But after this course, the system will just stay down, will not receive any submissions.
[01:30:58] Customer: The target metric will not work.
[01:30:58] Customer: I wonder if some other metric would be better to use in this case.
[01:30:58] Customer: It may be something about usability.
[01:32:00] Magel0n: Okay, no, I thought I had an idea, but it still falls to the same problems.
[01:32:20] Customer: Okay, okay.
[01:32:20] Customer: Like we can measure course adoption, which courses adopted the system.
[01:32:20] Customer: But we can't really influence this.
[01:32:20] Customer: Like, except for providing good service and inspiring others to use the system.
[01:32:20] Customer: So not sure if this can be a good metric either.
[01:32:20] Customer: But I don't know.
[01:32:20] Customer: If we consider like global adoption, like include the outside world, then we can somehow influence this.
[01:32:20] Customer: but like it will we could influence this by advertising this system like everywhere on reddit for example or hacker news and by providing good docs for it how to deploy and so on so this will But this is outside of the software engineering work.
[01:33:55] Magel0n: Yeah.
[01:34:00] Customer: And additionally, that will broaden the scope to a degree that is unmanageable in a little team.
[01:34:00] Customer: Yeah.
[01:34:00] Customer: So.
[01:34:00] Customer: Okay.
[01:34:00] Customer: Not users, not revenue.
[01:34:00] Customer: weekly submissions.
[01:34:00] Customer: I don't know, maybe a rating of students, like you, you, you can collect some.
[01:34:00] Customer: Yeah, some rating like how intuitive was it to use the system, and so on.
[01:34:00] Customer: shouldn't we try to connect the thresholds with at least some of our value propositions well yes and later and you will receive real students only later after the course finishes most probably so Okay, let's revise the VPS.
[01:35:33] Magel0n: It's practice the debugging skill, not the puzzle.
[01:35:33] Magel0n: It's fresh exercises on demand, not a stick set.
[01:35:33] Magel0n: It's debugging your own VS code, not a browser.
[01:35:33] Magel0n: And it's a public gallery of exercises.
[01:35:47] Customer: Fresh exercises on demand, not a fixed set.
[01:35:52] Magel0n: Perhaps we could go towards this, but that would violate a different decision that we have created, that the generation is teachers only.
[01:36:06] Customer: Yeah, but generation is not teachers only.
[01:36:06] Customer: It's students as well.
[01:36:06] Customer: They can generate problems for themselves.
[01:36:06] Customer: Just not upload them to the public gallery.
[01:36:36] Magel0n: Okay.
[01:36:36] Magel0n: So perhaps the new threshold that we could try to create is something like the number of generated exercises per active user.
[01:36:54] Customer: Well, but I assume that students will not really generate exercises.
[01:36:54] Customer: They will just try to solve as fast as possible what they are given and then leave the system.
[01:36:54] Customer: Okay.
[01:36:54] Customer: All right.
[01:36:54] Customer: So we are now discussing the focus metric, right?
[01:37:46] Magel0n: We're discussing a new threshold proposal that will be coming from a new focus metric.
[01:37:53] Customer: Okay.
[01:37:53] Customer: well if that is possible obviously yeah since it's not very possible maybe it would be better to consider some other metric like a focus metric can be like courses adoption like programming courses adoption but it's like for a longer term um It can also be like number of maintenance commits per year, so that the system does not die.
[01:37:53] Customer: It lives and is used by someone.
[01:37:53] Customer: If we measure it in students using the system, then the number may change, fluctuate, and And it's not completely clear which students will get more value.
[01:37:53] Customer: If the system is used with master students, will they get as much value as bachelor students?
[01:39:18] Magel0n: So perhaps we should truly do focus on long term course adoption and perhaps something like user experience as something closer to short term.
[01:39:32] Customer: I think, yeah, something like this.
[01:39:32] Customer: But, okay, I think, yeah, let's focus on students' satisfaction, like all users, teachers and students' satisfaction with the system, according to some metrics, some surveys, as our long-term goal.
[01:39:32] Customer: and accept that the threshold of success for the duration of this project, like mainly for this course, does not depend on the focus metric.
[01:39:32] Customer: Like you can get, well, actually it may depend But the scale will not be that much.
[01:39:32] Customer: The next assignment will ask you to prepare.
[01:39:32] Customer: usability test and the next number eight will ask you to conduct this usability test.
[01:39:32] Customer: You will get some metrics from users.
[01:39:32] Customer: You can measure the satisfaction somehow.
[01:39:32] Customer: And I think at that point, When you know that you are able to measure the satisfaction, you can make it your, and know how to do that.
[01:39:32] Customer: You can make this your focus metric and use, like set a threshold of success, like two, I don't know, like four out of five people are satisfied or something like this.
[01:39:32] Customer: But right now I'm not sure you have the right metrics in place.
[01:39:32] Customer: So I would suggest to change the focus metric a bit later if you have chosen something else.
[01:39:32] Customer: For now.
[01:39:32] Customer: Have you?
[01:42:00] Magel0n: Well, that's why we are here to discuss our choices.
[01:42:00] Magel0n: We have them as drafts.
[01:42:00] Magel0n: I have proposed them to you.
[01:42:00] Magel0n: What was it?
[01:42:00] Magel0n: What was it?
[01:42:00] Magel0n: The average, or not the average, the number of...
[01:42:00] Magel0n: Where is it?
[01:42:00] Magel0n: Yeah, yeah, yeah.
[01:42:00] Magel0n: The weekly sold decisions.
[01:42:00] Magel0n: You are right about saying that this is a little weird of a metric.
[01:42:28] Customer: Mm-hmm.
[01:42:28] Customer: Okay, some achievable metric is this, and yeah, is this satisfaction kinda what you need to, you can draft it for now, like how you're going to measure it, and then specify later when the exercises ask you.
[01:42:28] Customer: And so, yeah.
[01:42:28] Customer: And then based, and you, Okay.
[01:42:28] Customer: Yeah, that sounds like the way forward.
[01:43:20] Magel0n: Okay.
[01:43:20] Magel0n: So now, what?
[01:43:20] Magel0n: You have something more to say?
[01:43:23] Customer: Yeah.
[01:43:23] Customer: Okay, we have this core task for a student.
[01:43:23] Customer: But actually, I think we should consider an end-to-end scenario that it passes.
[01:43:23] Customer: Like operator deploys the system from the clean checkout, then adds the teacher's account, teacher logs in, creates an exercise, assigns, adds it to do the exercise set, assign the exercise set to students, which have to be also created by the operator in advance.
[01:43:23] Customer: Then students find the exercises in their dashboard or where they discovered them, like pool, solve a bit then the teacher updates and then like the students pull the changes, reconciliate with them with their local changes and then they submit they receive like the wrong verdict like wrong solution verdict then they fix something else receive like good solution correct solution verdict and then they see the verdict on the side and then the teacher downloads a csv or something like that for a group of students who were assigned this exercise set and successfully uploads it to Moodle for example or Or at least this CSV or a file with results passes some validation.
[01:43:23] Customer: That's guaranteed to pass the validation model.
[01:45:42] Magel0n: Okay, I think that for us it will be best to split it to well completing the core tasks end-to-end can be from different perspectives so to split it into learner to the teacher to the administrator as you have said yeah so yeah like if this scenario passes at the end yeah this is uh this will be a very important step towards success Okay.
[01:45:42] Magel0n: Do you have anything else to say?
[01:46:20] Customer: I don't think so.
[01:46:22] Magel0n: All right.
[01:46:22] Magel0n: So just checking in.
[01:46:22] Magel0n: For the thresholds of success, well, our primary goal is to Actualize them with all of the new findings that we have found throughout the progress that we've made to add the distinct separation between the learners, the teachers and whatnot to add that.
[01:46:22] Magel0n: Also, you have discussed regarding the additional changes for the structure itself with my colleague regarding like the commit changes, the sandboxing and whatnot, and our tries to implement it.
[01:46:22] Magel0n: And I think that is it for today.
[01:46:22] Magel0n: Yeah.
[01:46:22] Magel0n: Okay.
[01:46:22] Magel0n: well uh does my team have anything else to say well it doesn't seem so as i am getting well then very thank you very much for this productive meeting um yeah thank you as well for having me yeah and proceeding with the project All right.
[01:46:22] Magel0n: Bye-bye then.
[01:47:52] Customer: Yeah, goodbye.
[01:47:52] Customer: Have a nice evening.
[01:12:07] Tedor49: You too.
[01:47:52] Customer: Thanks.
