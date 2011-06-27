// Javascript code for Original SUpertris
// Copyright (C) 2011 Randall Cook. All Rights Reserved

window.onload = initAll;

var kBlockSize = 16;
var kBoardWidth = 11;
var kBoardHeight = 17;
var kNextWidth = 4;
var kNextHeight = 4;
var kLoopTime = 333; // milliseconds per game loop cycle

var gBoardCanvas = null;
var gBoardContext = null;
var gNextCanvas = null;
var gNextContext = null;
var gX = 0;
var gY = 0;
var gTimer = null;
var gLoopCount = 0;
var gTotalLoopTimeouts = 0;
var gPlaying = 0;

function initAll()
{
	// wire up the buttons and links
	document.getElementById("play").onclick = startGame;
	document.getElementById("left").onclick = moveLeft;
	document.getElementById("right").onclick = moveRight;
	document.getElementById("rotate").onclick = rotate;
	document.getElementById("drop").onclick = drop;
	
	// create the main board canvas
	gBoardCanvas = createCanvas(kBoardWidth * kBlockSize, kBoardHeight * kBlockSize);
	document.getElementById("boardArea").appendChild(gBoardCanvas);
	gBoardContext = gBoardCanvas.getContext("2d");

	// create the next piece canvas
	gNextCanvas = createCanvas(kNextWidth * kBlockSize, kNextHeight * kBlockSize);
	document.getElementById("nextArea").appendChild(gNextCanvas);
	gNextContext = gNextCanvas.getContext("2d");
}

function startGame()
{
	// reset game variables
	gX = (kBoardWidth / 2) >> 0;  // also ~~(x/y) or Math.floor(x/y) for integer division
	gY = 0;
	gLoopCount = 1;
	gTotalLoopTimeouts = kLoopTime;
	gPlaying = 1;
	
	// update the screen
	gBoardContext.clearRect(0, 0, gBoardCanvas.width, gBoardCanvas.height); // might also need to temporarily set the width to 1 and back again
	gBoardContext.fillRect(gX * kBlockSize, gY * kBlockSize, kBlockSize, kBlockSize);
	
	// grab keyboard focus
	
	// start the play loop
	gTimer = setTimeout("gameLoop()", kLoopTime);
	
	return false;
}

function gameLoop()
{
	// handle timer stuff
	if (gTimer)
	{
		clearTimeout(gTimer);
	}
	
	var loopStart = new Date();
	
	// move the piece down
	var oldY = gY;
	gY += 1;
	
	if (gY == kBoardHeight)
	{
		alert("Game Over! (" + gLoopCount + " loops, " + (gTotalLoopTimeouts / gLoopCount).toFixed(1) + " ms per loop)");
		gPlaying = 0;
		return;
	}
	
	// update the screen
	gBoardContext.clearRect(gX * kBlockSize, oldY * kBlockSize, kBlockSize, kBlockSize);
	gBoardContext.fillRect(gX * kBlockSize, gY * kBlockSize, kBlockSize, kBlockSize);
	
	// prepare for another loop
	var loopEnd = new Date();
	var elapsed = loopEnd.getTime() - loopStart.getTime();
	
	if (elapsed < kLoopTime)
	{
		var timeout = kLoopTime - elapsed;
		gTotalLoopTimeouts += timeout;
		gLoopCount += 1;
		gTimer = setTimeout("gameLoop()", timeout);
	}
	else
	{
		alert("System too slow!");
	}
}

function handleKey()
{
}

function moveLeft()
{
	if (gPlaying)
	{
		if (gX > 0)
		{
			gBoardContext.clearRect(gX * kBlockSize, gY * kBlockSize, kBlockSize, kBlockSize);
			gX -= 1;
			gBoardContext.fillRect(gX * kBlockSize, gY * kBlockSize, kBlockSize, kBlockSize);
		}
	}
	
	return false;
}

function moveRight()
{
	if (gPlaying)
	{
		if (gX < (kBoardWidth - 1))
		{
			gBoardContext.clearRect(gX * kBlockSize, gY * kBlockSize, kBlockSize, kBlockSize);
			gX += 1;
			gBoardContext.fillRect(gX * kBlockSize, gY * kBlockSize, kBlockSize, kBlockSize);
		}
	}
	
	return false;
}

function rotate()
{
	return false;
}

function drop()
{
	return false;
}

function createCanvas(width, height)
{
	var canvas = document.createElement("canvas");
	canvas.width = width;
	canvas.height = height;
	canvas.appendChild(document.createTextNode("HTML canvas not supported. Try a newer browser"));
	
	return canvas;
}
