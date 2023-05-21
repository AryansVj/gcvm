#include <windows.h>
#include <iostream>
#include <conio.h>

using namespace std;

int main()
{
	while (1)
	{
		cout<<"Enter cmd"<<endl;
        char g = getch();
		int x, y;
		POINT xypos;
 
       // Cursor will go to the entered position
        if (g == 'S' || g == 's')
		{
			cout<<"Enter the new position:"<<endl;                     //Enter position as seperated by space
			cin>>x>>y;
			SetCursorPos(x, y);
		}

		else if (g == 'g' || g == 'G')
		{
			GetCursorPos(&xypos);
			cout<<"X:"<<xypos.x<<"\tY:"<<xypos.y<<endl;
		}
        

		else if (g == 'x' || g == 'X')
		{
			break;
		}

        

    }

}