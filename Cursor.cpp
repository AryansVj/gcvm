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

        if (g == 'S' || g == 's')
		{
			cout<<"Enter the new position:"<<endl;
			cin>>x>>y;
			SetCursorPos(x, y);
		}

		else if (g == 'g' || g == 'G')
		{
			GetCursorPos(&xypos);
			cout<<"X:"<<xypos.x<<"\tY:"<<xypos.y<<endl;
		}




    }

}