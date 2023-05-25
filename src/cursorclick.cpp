#include <windows.h>
#include <iostream>
#include <conio.h>

using namespace std;

int main()
{
	cout<<"Press 'F' for Left Click"<<endl;//0x46
	cout<<"Press 'G' for Right Click"<<endl;//0x47
	
	while (1)
	{
		if (GetAsyncKeyState(0x01))
		{
			cout<<"Left click pressed"<<endl;
		}
		else if (GetAsyncKeyState(0x02))
		{
			cout<<"Right click pressed"<<endl;
		}
		else if (GetAsyncKeyState(0x46))
		{
			mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0);
			Sleep(100);
			mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, 0);
		}
		else if (GetAsyncKeyState(0x47))
		{
			mouse_event(MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0);
			Sleep(100);
			mouse_event(MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0);
		}
	}
	
	getch();
}

/*
#define MOUSEEVENTF_MOVE 0x0001
#define MOUSEEVENTF_LEFTDOWN 0x0002
#define MOUSEEVENTF_LEFTUP 0x0004
#define MOUSEEVENTF_RIGHTDOWN 0x0008
#define MOUSEEVENTF_RIGHTUP 0x0010
#define MOUSEEVENTF_MIDDLEDOWN 0x0020
#define MOUSEEVENTF_MIDDLEUP 0x0040
#define MOUSEEVENTF_XDOWN 0x0080
#define MOUSEEVENTF_XUP 0x0100
#define MOUSEEVENTF_WHEEL 0x0800
#define MOUSEEVENTF_VIRTUALDESK 0x4000
#define MOUSEEVENTF_ABSOLUTE 0x8000
*/
