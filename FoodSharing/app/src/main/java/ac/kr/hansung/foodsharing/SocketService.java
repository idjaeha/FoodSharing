package ac.kr.hansung.foodsharing;

import android.app.Service;
import android.content.ComponentName;
import android.content.Intent;
import android.os.IBinder;
import android.util.Log;

import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.net.Socket;

public class SocketService extends Service {
    private final static String addr = "192.168.0.36";
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
        if (intent == null) {
            return Service.START_STICKY;
        } else {
            processCommand(intent);
        }

        return super.onStartCommand(intent, flags, startId);
    }

    public void processCommand(Intent intent) {
        String command = intent.getStringExtra("command");

        if (command == "1") {
            socket.sendMsg("hello world!!!");
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
            sendMsg("hello python!!!");
            sendMsg("hello python!!!");
            socketAlive = true;
            while (true) {
                try {
                    byte[] b = new byte[128];
                    dis.read(b);
                    String receivedMsg = new String(b);
                    receivedMsg = receivedMsg.trim();

                    Log.d("MainActivity", "서버에서 받은 메세지 : " + receivedMsg);
                } catch (Exception e) {
                    e.printStackTrace();
                }
            }
        }

        public void sendMsg(String msg) {
            Log.d("MainActivity", msg.trim() + "메세지 전송");
            try {
                dos = new DataOutputStream(soc.getOutputStream());
                byte[] sendMsgByte = new byte[128];
                String s = String.format("%-128s", msg.trim());
                sendMsgByte = s.getBytes("euc-kr");
                dos.write(sendMsgByte);
            } catch (Exception e) {
                e.printStackTrace();
                Log.d("MainActivity", msg.trim() + "메세지 전송 실패");
            }
        }

        public boolean isSocketAlive() {
            return socketAlive;
        }
    }
}
