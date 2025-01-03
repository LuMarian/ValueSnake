## What is ValueSnake

First of all, I am just a Data guy, not a Dev, so I am not in the software security dependencies or whatever business. So I have no clue if there is anything in the background of these apps that might become vulnerable in the future. It will not be regularly maintained, not do I take any responsibility for any issues that might arise in the future. Just to be sure... :)

These applications or plugins are designed as a simple extension/improvement for the current use with [OpenSkyPlus](https://github.com/OpenSkyPlus/OpenSkyPlus) (1.1.1) and the [Springbok (MLM2PRO) Connector](https://github.com/springbok/MLM2PRO-GSPro-Connector) (1.10.16) for Using a separate Putting method (like ExPutt) in GSPro.
The name comes from a quick first draft random name “ValueKing”, that my brother made in C# and my implementation in the easiest way possible – python – hence “Snake”.
I have built upon the OpenSkyPlus Framework and simply modified the code slightly for it to work. I don’t want to repost the whole project, nor do I want to start a pull request as this feature is very specific to people using Springbok, so I am only posting the updated .dll files. Regarding ValueSnake, I have shared the source code which is really not that impressive and on which I will be very happy to take improvements for.

## What does it do?

After you set up the files, when you hit a shot, it will be transferred to the ValueSnake window, where it can be read by Springbok. Before the first shot, the ValueSnake window will be black, so no worries :)

Generally, the files here on ValueSnake do 3 things:

•	Improve on ghost reads by the SkyTrak+, meaning that stupidly out of range values for launch or speed, that happen on those accidental triggers occasionally, will be discarded: > 70° Launch, < 3 mph Ballspeed and Spin < 400 rpm.

•	Send the shot data to localhost:8080/wurstbrot (sorry to vegans…) instead of OpenAPI directly. The last thing I fixed was that the SkyTrak Range will not register short ship shots, so I had to either “Force Monitor Arm” or “Force Normal Mode” within the OpenSkyPlus Windon in SkyTrak. That is now fixed as there is an automatic 10 second Re-Arm timer after every registered shot. It worked fine for me when I tested.

•	Receive the shot data in the “ValueSnake” application and display them without delay in a way that can be read by the Springbok Connector.
Please note that the Auto Switch to PuttingMode is not working with this setup, your putting will happen somewhere else anyway and if you ever need a super shot chip shot, just “Force Putting Mode” in the OpenSkyPlus window. This could be fixed in a future version but for that I would also need to touch the MLM2PRO connector code and I’m not sure that’s going to be a thing.

## HowTo
A possible example for a setup is the “original” OpenSkyPlus together with SkyTrak 4.4.7. Rename (SkyTrak447) and zip this folder and Install another SkyTrak 4.x version, for example SkyTrak 4.4.2. Rename this to SkyTrak442, Unzip SkyTrak447 and you now have two versions of SkyTrak installed. Inside of SkyTrak442, you use the same OpenSkyPlus as in SkyTrak447, but replace the .dll files inside of the existing BepInEx subfolders with the ones from here. Make sure you put the OpenSkyPlus one and GSPro4OSP in the respective folders.
From there, you download Springbok (the MLM2PRO) Connector as linked at the top and when setting up your device, make sure you call the window to screen capture “ValueSnake”. Apart from that just set it up as described in their instructional videos and voilà:

You now have two SkyTrak options. Start 4.4.7 if you just want to play with your SkyTrak+, maybe do some AutoPutt play or simply practice on the range. Start 4.4.2 and Springbok (which, if correctly setup will start your Camera and ValueSnake) if you want to have the full playing experience.
Make sure you use *fskit* as your selected launch monitor type in Springbok as this is the font and style (white numbers on black background) that is used for the display of the numbers. If you don’t have that version of [Stratos](https://fonts.adobe.com/fonts/stratos) as a font, make sure you get it installed, or at least have your numbers look somewhat like what you find when you google for the Full Swing Kit App.
To install, one might use the Adobe Font library – The fonts being used are Stratos Regular and Stratos Bold Italic. I found [a tool](https://badnoise.net/TypeRip/) that allows font download but I am not an expert in that, so yeah.

## Random Stuff

•	If you use an ExPutt, don’t setup your ball in the correct spot for putting while you’re hitting your other shots. It will very likely get a misread during that time and as soon as you switch to putting mode it will get a misread and the ball either goes 0.1m or 20m. Only put your ball in the correct spot before you want to putt and you should virtually never get any accidental read.

•	I will be monitoring any wild accidental or misreads by my SkyTrak+ in the future and if I see any distinctive patterns that are exclusive to apparent misreads, they will be added to ValueSnake. If you feel like you have regular misread patterns (I am talking about a 50 yd Slice with a Wedge or so, not a “I hit that one perfect, that was never 10 m right of the pin”), don’t hesitate to text me on Discord! I’d be happy to check them out and implement them as well

•	Because OpenSkyPlus is now not directly communicating with GSPro any more you lose the ability to switch to putting mode for short chip shots. Actually never bothered me when playing so far though
