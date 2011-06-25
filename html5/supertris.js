// Javascript code for Original SUpertris
// Copyright (C) 2011 Randall Cook. All Rights Reserved

window.onload = initAll;
var kBlockSize = 16;
var kBoardWidth = 11;
var kBoardHeight = 17;
var kNextWidth = 4;
var kNextHeight = 4;
var gBoardCanvas = null;
var gNextCanvas = null;

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

	// create the next piece canvas
	gNextCanvas = createCanvas(kNextWidth * kBlockSize, kNextHeight * kBlockSize);
	document.getElementById("nextArea").appendChild(gNextCanvas);
}

function startGame()
{
	alert("let's go!");
	
	// reset game variables
	
	// update the screen
	
	// grab keyboard focus
	
	// start the play loop
	
	return false;
}

function handleKey()
{
}

function moveLeft()
{
	return false;
}

function moveRight()
{
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
