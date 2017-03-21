// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed.
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.

//while(1)
//{
//    if(RAM[24576])black;
//    else white;
//}
(LOOP)
    @SCREEN
    D=A
    @i
    M=D

    @KBD
    D=M
    @BLACK
    D;JGT
    @WHITE
    D;JEQ

(BLACK)
    @i
    A=M
    M=-1
    @i
    M=M+1
    D=M
    @KBD
    D=A-D
    @BLACK
    D;JGT
    @LOOP
    0;JMP

(WHITE)
    @i
    A=M
    M=0
    @i
    M=M+1
    D=M
    @KBD
    D=A-D
    @BLACK
    D;JGT
    @LOOP
    0;JMP
