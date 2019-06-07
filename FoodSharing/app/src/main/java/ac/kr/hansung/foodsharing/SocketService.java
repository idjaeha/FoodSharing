package ac.kr.hansung.foodsharing;

import android.app.Service;
import android.content.Intent;
import android.os.Bundle;
import android.os.IBinder;
import android.os.Message;
import android.util.Log;
import android.widget.Toast;

import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.net.Socket;

import static ac.kr.hansung.foodsharing.ChatActivity.chatHandler;
import static ac.kr.hansung.foodsharing.InitActivity.mobileInfo;

public class SocketService extends Service {
    public static String addr = "192.168.0.36";
    public static int port = 10000;
    final int BUFSIZE = 512;
    ConnectThread socket;
    static public SocketService mySocketService;

    public SocketService() {
        mySocketService = this;
    }

    @Override
    public IBinder onBind(Intent intent) {
        // TODO: Return the communication channel to the service.
        throw new UnsupportedOperationException("Not yet implemented");
    }

    @Override
    public void onCreate() {
        super.onCreate();

        //서버와 연결을 합니다.
        socket = new ConnectThread();
        socket.start();
    }

    @Override
    public int onStartCommand(Intent intent, int flags, int startId) {
        Log.d("SocketService", "onStartCommand 실행 : " + intent.getStringExtra("command"));
        if (intent == null) {
            return Service.START_STICKY;
        } else {
            processCommand(intent);
        }

        return super.onStartCommand(intent, flags, startId);
    }

    public void processCommand(Intent intent) {
        String command = intent.getStringExtra("command");

        //null 값이면
        if (command == null) {
            Log.d("SocketService", "cmd 값이 null입니다.");
            return;
        }

        if (command.equals("0")) {
            //연결 확인
            String msg = "0//";
            socket.sendMsg(msg);
        } else if (command.equals("1") == true) {
            //로그인 요청
            String msg = "1//" + intent.getStringExtra("id") + "//" + intent.getStringExtra("pwd") + "//";
            socket.sendMsg(msg);
        } else if (command.equals("3") == true) {
            //top5 요청
            String msg = "3//";
            socket.sendMsg(msg);
        } else if (command.equals("5") == true) {
            //가게 목록 요청
            if (intent.getStringExtra("flag").equals("0")) {
                String msg = "5//0//" + intent.getStringExtra("category") + "//";
                socket.sendMsg(msg);
            } else if (intent.getStringExtra("flag").equals("1")) {
                String msg = "5//1//" + intent.getStringExtra("food_name") + "//";
                socket.sendMsg(msg);
            }
        } else if (command.equals("7")) {
            String msg = "7//" + intent.getIntExtra("rest_num", 0) + "//";
            socket.sendMsg(msg);
        } else if (command.equals("9")) {
            String msg = "9//" + intent.getIntExtra("food_num", 0) + "//" + mobileInfo.userNum + "//" + mobileInfo.nickName + "//";
            socket.sendMsg(msg);
            mobileInfo.foodNum = intent.getIntExtra("food_num", 0);
        } else if (command.equals("11")) {
            // 메시지 전송
            String msg = intent.getStringExtra("msg");
            socket.sendMsg(msg);
        } else if (command.equals("13")) {
            // 채팅방 나가기 요청
            int foodNum = intent.getIntExtra("food_num", -1);
            String nickName = mobileInfo.nickName;
            String msg = "13//" + foodNum + "//" + nickName + "//";
            socket.sendMsg(msg);
        } else if (command.equals("15")) {
            //user top5 요청
            String msg = "15//" + intent.getIntExtra("user_num", -1);
            socket.sendMsg(msg);
        } else if (command.equals("20")) {
            //로그아웃
            String msg = "20//" +  intent.getIntExtra("user_num", -1) + "//";
            socket.sendMsg(msg);
            mobileInfo = new MobileInfo(-1,"","");
        } else if (command.equals("100")) {
            String msg = "100//" + intent.getStringExtra("category") + "//" + mobileInfo.userNum + "//";
            socket.sendMsg(msg);
        }
    }

    @Override
    public void onDestroy() {
        super.onDestroy();
    }

    class ConnectThread extends Thread {
        Socket soc = null;
        DataOutputStream dos;
        DataInputStream dis;
        public void run() {
            try {
                soc = new Socket(addr, port);
                dos = new DataOutputStream(soc.getOutputStream());
                dis = new DataInputStream(soc.getInputStream());
                mobileInfo.isSocketStart = true;
                Log.d("SocketService", "정상 접속 성공");
            } catch (Exception e) {
                e.printStackTrace();
                Log.d("SocketService", "정상 접속 실패");
                interrupt();
                return;
            }

            while (true) {
                try {
                    if (soc != null) {
                        byte[] b = new byte[BUFSIZE];
                        dis.read(b);
                        String receivedMsg = new String(b, "euc-kr");
                        receivedMsg = receivedMsg.trim();
                        Log.d("SocketService", "서버에서 받은 메세지 : " + receivedMsg);
                        processRecvMsg(receivedMsg);


                    } else {
                        break;
                    }
                } catch (Exception e) {
                    e.printStackTrace();
                    Log.d("SocketService", "서버와 연결 종료");
                    break;
                }
            }
        }

        public void processRecvMsg(String msg) {
            msg = msg.trim();
            String[] msgArr = msg.split("//");
            String cmd = msgArr[0];

            if (cmd.equals("0")) {
                //연결 확인
                mobileInfo.isConnectServer = true;
            } else if (cmd.equals("2")) {
                //로그인 응답
                if (msgArr[1].equals("1")) {
                    mobileInfo.setUserNum(Integer.parseInt(msgArr[2]));
                    mobileInfo.setId(msgArr[3]);
                    mobileInfo.setPwd(msgArr[4]);

                    Intent nextIntent = new Intent(getApplicationContext(), MainActivity.class);
                    nextIntent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
                    startActivity(nextIntent);
                }
            } else if (cmd.equals("4")) {
                //top5 응답
                String[] temp = {msgArr[1], msgArr[2], msgArr[3], msgArr[4], msgArr[5]};
                mobileInfo.setTop5Food(temp);
            } else if (cmd.equals("6")) {
                //가게 목록 응답
                String flag = msgArr[1];
                int num = Integer.parseInt(msgArr[2]);
                Intent nextIntent = new Intent(getApplicationContext(), StoreListActivity.class);
                nextIntent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
                nextIntent.putExtra("num", num);
                for (int i = 0; i < num; i++) {
                    int restNum = Integer.parseInt(msgArr[3 + 5 * i]);
                    String restName = msgArr[4 + 5 * i];
                    String categoryName = msgArr[5 + 5 * i];
                    float fRestX = Float.parseFloat(msgArr[6 + 5 * i]);
                    float fRestY = Float.parseFloat(msgArr[7 + 5 * i]);
                    int restX = (int) fRestX;
                    int restY = (int) fRestY;
                    nextIntent.putExtra("rest_num" + i, restNum);
                    nextIntent.putExtra("rest_name" + i, restName);
                    nextIntent.putExtra("category_name" + i, categoryName);
                    nextIntent.putExtra("rest_x" + i, restX);
                    nextIntent.putExtra("rest_y" + i, restY);
                }
                startActivity(nextIntent);
            } else if (cmd.equals("8")) {
                //가게 내의 음식 목록 응답
                int num = Integer.parseInt(msgArr[1]);
                String title = msgArr[2];
                Intent nextIntent = new Intent(getApplicationContext(), MenuActivity.class);
                nextIntent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
                nextIntent.putExtra("num", num);
                nextIntent.putExtra("title", title);
                for (int i = 0; i < num; i++) {
                    int foodNum = Integer.parseInt(msgArr[3 + 2 * i]);
                    String foodName = msgArr[4 + 2 * i];
                    nextIntent.putExtra("food_num" + i, foodNum);
                    nextIntent.putExtra("food_name" + i, foodName);
                }
                startActivity(nextIntent);
            } else if (cmd.equals("10")) {
                //채팅방 입장 응답
                String title = msgArr[1];
                String subTitle = msgArr[2];
                int num = Integer.parseInt(msgArr[3]);
                String nickName = msgArr[4];
                int flag = Integer.parseInt(msgArr[5]);

                if(flag == 1) {
                    Intent nextIntent = new Intent(getApplicationContext(), ChatActivity.class);
                    nextIntent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
                    nextIntent.putExtra("rest_name", title);
                    nextIntent.putExtra("food_name", subTitle);
                    nextIntent.putExtra("nick_name", subTitle);
                    nextIntent.putExtra("num", num);
                    startActivity(nextIntent);
                } else if (flag == 0) {
                    //남은 인원에게 알림
                    Bundle data = new Bundle();
                    Message alertMsg = new Message();
                    data.putString("command", "enter");
                    data.putInt("num", num);
                    data.putString("nick_name", nickName);
                    alertMsg.setData(data);
                    chatHandler.sendMessage(alertMsg);
                }
            } else if (cmd.equals("11")) {
                //메시지 전송 응답
                int userNum = Integer.parseInt(msgArr[1]);
                String userNickName = msgArr[2];
                String userMsg = msgArr[4];

                //채팅방으로 내용 전송
                Bundle data = new Bundle();
                Message chatMsg = new Message();
                data.putString("msg", userMsg);
                data.putString("command","msg");
                data.putString("nick_name", userNickName);
                data.putInt("user_num", userNum);
                chatMsg.setData(data);
                chatHandler.sendMessage(chatMsg);

                Log.d("SocketService", msg);
            } else if (cmd.equals("14")) {
                //채팅방 나가기 응답
                int num = Integer.parseInt(msgArr[1]);
                String nickName = msgArr[2];

                //남은 인원에게 알림
                Bundle data = new Bundle();
                Message alertMsg = new Message();
                data.putString("command", "exit");
                data.putInt("num", num);
                data.putString("nick_name", nickName);
                alertMsg.setData(data);
                chatHandler.sendMessage(alertMsg);

                Log.d("SocketService", msg);
            } else if (cmd.equals("16")) {
                //top5 응답
                String[] temp = {msgArr[1], msgArr[2], msgArr[3], msgArr[4], msgArr[5]};
                mobileInfo.setUserTop5Food(temp);
            }

        }

        public void sendMsg(String msg) {
            Log.d("SocketService", "메세지 전송 : " + msg.trim());
            class SendMsg implements Runnable {
                String msg;
                public SendMsg(String msg) {
                    this.msg = msg;
                }

                public void run() {
                    try {
                        if (soc != null) {
                            //dos = new DataOutputStream(soc.getOutputStream());
                            byte[] sendMsgByte = new byte[BUFSIZE];
                            String s = String.format("%-512s", msg.trim());
                            sendMsgByte = s.getBytes("euc-kr");
                            dos.write(sendMsgByte);
                        } else {
                            Log.d("SocketService", "소켓이 null 값입니다.");
                        }
                    } catch (Exception e) {
                        e.printStackTrace();
                        Log.d("SocketService", msg.trim() + "메세지 전송 실패");
                    }
                }
            }
            Thread sm = new Thread(new SendMsg(msg));
            sm.start();
        }
    }
}
