// Javascript code for Original SUpertris
// Copyright (C) 2011 Randall Cook. All Rights Reserved

/*
 * Data Structures
 * 
 * Board
 * The board is a 2D array of integers, where zero means empty, negative 
 * numbers are game-generated pieces, and positive numbers are user-generated 
 * pieces. Until I learn how to use multidimensional arrays in JavaScript, 
 * I'll use a simple 1D array and compute offsets manually.
 * 
 * Piece
 * A piece contains several attributes: a list of relative offsets from 
 * its current position where it extends (extents), a name for itself, 
 * a reference to the piece it should rotate into. Each extent consists 
 * of X and Y offsets, and a reference to the image to display on screen.
 * 
 * Active Piece
 * There is a master list of pieces that should not change. The active 
 * piece, which is the one currently falling, consists of X and Y board 
 * coordinates, an ID number to distinguish it from other pieces on the 
 * board, and a reference to the reference piece that it is.
 */

window.onload = initAll;

// constants
var kBlockSize = 16;
var kBoardWidth = 11;
var kBoardHeight = 17;
var kBoardArea = kBoardWidth * kBoardHeight;
var kNextWidth = 4;
var kNextHeight = 4;
var kNextArea = kNextWidth * kNextHeight;
var kLoopTime = 333; // milliseconds per game loop cycle

// pieces
var stick_h = createPiece([-2, -1, 0, 1], [0, 0, 0, 0]);
var stick_v = createPiece([0, 0, 0, 0], [-2, -1, 0, 1]);
var square = createPiece([-1, 0, -1, 0], [-1, -1, 0, 0]);
var S_h = createPiece([1, 0, 0, -1], [-1, -1, 0, 0]);
var S_v = createPiece([-1, -1, 0, 0], [-1, 0, 0, 1]);
var Z_h = createPiece([-1, 0, 0, 1], [-1, -1, 0, 0]);
var Z_v = createPiece([1, 1, 0, 0], [-1, 0, 0, 1]);
var J_1 = createPiece([-1, 0, 0, 0], [0, 0, -1, -2]);
var J_2 = createPiece([0, 0, -1, -2], [0, -1, -1, -1]);
var J_3 = createPiece([0, -1, -1, -1], [-1, -1, 0, 1]);
var J_4 = createPiece([-1, -1, 0, 1], [-1, 0, 0, 0]);
var L_1 = createPiece([0, -1, -1, -1], [0, 0, -1, -2]);
var L_2 = createPiece([0, 0, -1, -2], [-1, 0, 0, 0]);
var L_3 = createPiece([-1, 0, 0, 0], [-1, -1, 0, 1]);
var L_4 = createPiece([-1, -1, 0, 1], [0, -1, -1, -1]);
var T_1 = createPiece([-1, 0, 1, 0], [0, 0, 0, 1]);
var T_2 = createPiece([0, 0, 0, 1], [-1, 0, 1, 0]);
var T_3 = createPiece([-1, 0, 1, 0], [0, 0, 0, -1]);
var T_4 = createPiece([0, 0, 0, -1], [-1, 0, 1, 0]);
stick_h.next = stick_v;
stick_v.next = stick_h;
square.next = square;
S_h.next = S_v;
S_v.next = S_h;
Z_h.next = Z_v;
Z_v.next = Z_h;
J_1.next = J_2;
J_2.next = J_3;
J_3.next = J_4;
J_4.next = J_1;
L_1.next = L_2;
L_2.next = L_3;
L_3.next = L_4;
L_4.next = L_1;
T_1.next = T_2;
T_2.next = T_3;
T_3.next = T_4;
T_4.next = T_1;
var gPieces = [stick_h, square, S_h, Z_h, J_1, L_1, T_1];

// game variables
var gBoardCanvas = null;
var gBoardContext = null;
var gNextCanvas = null;
var gNextContext = null;
var gX = 0;
var gY = 0;
var gTimer = null;
var gLoopCount = 0;
var gTotalLoopTimeouts = 0;
var gPlaying = false;
var gActivePiece = null;

function initAll()
{
	// wire up the buttons and links
	document.getElementById("play").onclick = startGame;
	document.getElementById("left").onclick = moveLeft;
	document.getElementById("right").onclick = moveRight;
	document.getElementById("rotate").onclick = rotate;
	document.getElementById("drop").onclick = drop;
	
	document.onkeypress = handleKey;
	
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
	if (gPlaying == true)
	{
		return false;
	}
	
	// reset game variables
	gLoopCount = 1;
	gTotalLoopTimeouts = kLoopTime;
	gPlaying = true;
	gActivePiece = gPieces[randomInt(gPieces.length)];
	gX = (kBoardWidth / 2) >> 0;  // also ~~(x/y) or Math.floor(x/y) for integer division
	gY = 0 - gActivePiece.minY;
	
	// update the screen
	gBoardContext.clearRect(0, 0, gBoardCanvas.width, gBoardCanvas.height); // might also need to temporarily set the width to 1 and back again
	plotActivePiece();
	
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
	var moveSuccess = moveActivePiece(0, 1, false);

	// handle the case when we cannot move the piece down
	if (moveSuccess == false)
	{
		alert("Game Over! (" + gLoopCount + " loops, " + (gTotalLoopTimeouts / gLoopCount).toFixed(1) + " ms per loop)");
		gPlaying = false;
		return;
	}
	
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

function handleKey(event)
{
	//alert("key pressed:" + event.charCode);
	document.getElementById("debug").innerHTML = "charCode: " + event.charCode;
	// j, k, l = 106, 107, 108
	if (event.charCode == 106 || event.charCode == 74)
	{
		moveLeft();
	}
	else if (event.charCode == 107 || event.charCode == 75)
	{
		rotate();
	}
	else if (event.charCode == 108 || event.charCode == 76)
	{
		moveRight();
	}
	else if (event.charCode == 32)
	{
		drop();
	}
	else if (event.charCode == 112 || event.charCode == 80)
	{
		startGame();
	}
}

function moveLeft()
{
	if (gPlaying)
	{
		moveActivePiece(-1, 0, false);
	}
	
	return false;
}

function moveRight()
{
	if (gPlaying)
	{
		moveActivePiece(1, 0, false);
	}
	
	return false;
}

function rotate()
{
	if (gPlaying)
	{
		moveActivePiece(0, 0, true);
	}
	
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

function createPiece(x_extents, y_extents)
{
	if (x_extents.length != y_extents.length)
	{
		alert("different lengths");
		return null;
	}
	
	piece = new Object;
	
	piece.x_extents = x_extents;
	piece.y_extents = y_extents;

	piece.minX = minValue(x_extents);
	piece.maxX = maxValue(x_extents);
	piece.minY = minValue(y_extents);
	piece.maxY = maxValue(y_extents);
	
	/*
	s = "extents:";
	for (var i = 0; i < x_extents.length; i++)
	{
		s += " " + x_extents[i] + "," + y_extents[i];
	}
	alert(s);
	*/
	
	return piece;
}

function moveActivePiece(deltaX, deltaY, rotate)
{
	var i, x, y;
	
	// verify that we can move the piece
	for (i = 0; i < gActivePiece.x_extents.length; i++)
	{
		x = gX + deltaX + gActivePiece.x_extents[i];
		y = gY + deltaY + gActivePiece.y_extents[i];
		
		if (getBoardID(x, y) != 0)
		{
			return false;
		}
	}
	
	// erase the current piece
	for (i = 0; i < gActivePiece.x_extents.length; i++)
	{
		x = gX + gActivePiece.x_extents[i];
		y = gY + gActivePiece.y_extents[i];
		
		gBoardContext.clearRect(x * kBlockSize, y * kBlockSize, kBlockSize, kBlockSize);
	}
	
	// apply the transformation
	gX += deltaX;
	gY += deltaY;
	
	if (rotate)
	{
		gActivePiece = gActivePiece.next;
	}
	
	// draw the piece in the new location
	plotActivePiece()
	
	// indicate that we moved the piece
	return true;
}

function plotActivePiece()
{
	for (var i = 0; i < gActivePiece.x_extents.length; i++)
	{
		var x = gX + gActivePiece.x_extents[i];
		var y = gY + gActivePiece.y_extents[i];
		
		gBoardContext.fillRect(x * kBlockSize, y * kBlockSize, kBlockSize, kBlockSize);
	}
}

function getBoardID(x, y)
{
	if (x < 0 || x >= kBoardWidth)
	{
		return -1;
	}
	
	if (y < 0 || y >= kBoardHeight)
	{
		return -1;
	}
	
	return 0;
}

function randomInt(range)
{
	// It might be worthwhile to check for Math.random returning 1.0, 
	// which would violate the [0, range) expected behavior, and to 
	// enforce limits on the input range as well.
	
	return Math.floor(range * Math.random());
}

function minValue(a)
{
	var minimum = a[0];
	
	for (var i = 1; i < a.length; i++)
	{
		if (a[i] < minimum)
		{
			minimum = a[i];
		}
	}
	
	return minimum;
}

function maxValue(a)
{
	var maximum = a[0];
	
	for (var i = 1; i < a.length; i++)
	{
		if (a[i] > maximum)
		{
			maximum = a[i];
		}
	}
	
	return maximum;
}
