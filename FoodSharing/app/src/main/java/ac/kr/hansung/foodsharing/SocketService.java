package ac.kr.hansung.foodsharing;

import android.app.Service;
import android.content.ComponentName;
import android.content.Context;
import android.content.Intent;
import android.os.IBinder;
import android.util.Log;

import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.net.Socket;

import static ac.kr.hansung.foodsharing.InitActivity.userInfo;

public class SocketService extends Service {
    private final static String addr = "192.168.0.7";
    private final static int port = 10000;
    ConnectThread socket;

    public SocketService() {
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
        Log.d("MainActivity", "onStartCommand 실행 : " + intent.getStringExtra("command"));
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
            return;
        }

        if (command.equals("1") == true) {
            String msg = "1//" + intent.getStringExtra("id") + "//" + intent.getStringExtra("pwd") + "//";
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
        boolean socketAlive = false;
        public void run() {
            try {
                soc = new Socket(addr, port);
                dos = new DataOutputStream(soc.getOutputStream());
                dis = new DataInputStream(soc.getInputStream());
            } catch (Exception e) {
                e.printStackTrace();
                Log.d("MainActivity", "정상 접속 실패");
                interrupt();
                return;
            }
            socketAlive = true;
            while (true) {
                try {
                    byte[] b = new byte[128];
                    dis.read(b);
                    String receivedMsg = new String(b);
                    receivedMsg = receivedMsg.trim();
                    processRecvMsg(receivedMsg);

                    Log.d("MainActivity", "서버에서 받은 메세지 : " + receivedMsg);
                } catch (Exception e) {
                    e.printStackTrace();
                    Log.d("MainActivity", "서버와 연결 종료");
                    break;
                }
            }
        }

        public void processRecvMsg(String msg) {
            msg = msg.trim();
            String[] msgArr = msg.split("//");
            String cmd = msgArr[0];
            if (cmd.equals("2")) {
                if (msgArr[1].equals("1")) {
                    userInfo.setUserNum(Integer.parseInt(msgArr[1]));
                    userInfo.setId(msgArr[2]);
                    userInfo.setPwd(msgArr[3]);

                    Intent nextIntent = new Intent(getApplicationContext(), MainActivity.class);
                    nextIntent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
                    startActivity(nextIntent);
                }
            }

        }

        public void sendMsg(String msg) {
            Log.d("MainActivity", "메세지 전송 : " + msg.trim());
            class SendMsg implements Runnable {
                String msg;
                public SendMsg(String msg) {
                    this.msg = msg;
                }

                public void run() {
                    try {
                        if (soc != null) {
                            //dos = new DataOutputStream(soc.getOutputStream());
                            byte[] sendMsgByte = new byte[128];
                            String s = String.format("%-128s", msg.trim());
                            sendMsgByte = s.getBytes("euc-kr");
                            dos.write(sendMsgByte);
                        } else {
                            Log.d("MainActivity", "소켓이 null 값입니다.");
                        }
                    } catch (Exception e) {
                        e.printStackTrace();
                        Log.d("MainActivity", msg.trim() + "메세지 전송 실패");
                    }
                }
            }
            Thread sm = new Thread(new SendMsg(msg));
            sm.start();
        }

        public boolean isSocketAlive() {
            return socketAlive;
        }
    }
}
