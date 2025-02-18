#if 1//42分暴力
#define _CRT_SECURE_NO_WARNINGS
#include<iostream>
#include<cstdio>
#include<cstring>
#include<queue>
//#include<algorithm>
using std::cout;
using std::cin;
using std::endl;
struct coor {
	int x;
	int y;
	int t;
	coor() : x(0), y(0), t(0) {
	}
};
int dx[5] = { 0,1,0,-1,0 };
int dy[5] = { 0,0,1,0,-1 };
std::queue<coor> que;
int map[320][320];
int main() {
	std::memset(map, -1, sizeof(map));//无奈数据范围是0-1000
	int temp,x,y,n;
	cin >> n;
	for (int i = 1; i <= n; i++) {
		scanf("%d %d %d",&x,&y,&temp);
		for (int j = 0; j <= 4; j++) {
			if (x + dx[j] >= 0 && y + dy[j] >= 0) {
				map[x + dx[j]][y + dy[j]] =
					(-1 == map[x + dx[j]][y + dy[j]]) ?
					temp : std::min(map[x + dx[j]][y + dy[j]], temp);
			}
		}
	}
	/*
	for (int i = 0; i <= 5; i++) {
		for (int j = 0; j <= 5; j++)
			cout << map[i][j]<<" ";
		cout << endl;
	}
	*/
	coor  start, now;
	que.push(start);
	map[start.x][start.y] = -2;
	while (0 == que.empty()) {
		start = que.front();
		que.pop();
		for (int i = 1; i <= 4; i++) {
			now.x = start.x + dx[i];
			now.y = start.y + dy[i];
			now.t = start.t + 1;//前景与时间同步			
			if (now.x >= 0 && now.y >= 0) {//不越界
				if (map[now.x][now.y] > now.t&&
					map[now.x][now.y]!=-2)//未来有陨石撞击
				{
					map[now.x][now.y] = -2;//标记为走过
					que.push(now);  //暂时安全	
				}
				else if(-1== map[now.x][now.y]){//绝对安全未来没有陨石撞击
					cout<<now.t;
					return 0;
				}
			}

		}
	}
	cout << "-1";
	return (0);
}

#endif 