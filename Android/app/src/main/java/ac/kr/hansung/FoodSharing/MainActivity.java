package ac.kr.hansung.FoodSharing;

import android.content.pm.PackageInfo;
import android.content.pm.PackageManager;
import android.content.pm.Signature;
import android.os.Bundle;
import android.support.annotation.NonNull;
import android.support.design.widget.BottomNavigationView;
import android.support.v4.app.FragmentManager;
import android.support.v4.app.FragmentTransaction;
import android.support.v7.app.AppCompatActivity;
import android.util.Base64;
import android.util.Log;
import android.view.MenuItem;

import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.net.Socket;
import java.security.MessageDigest;


public class MainActivity extends AppCompatActivity {

    FragmentManager fm;
    FragmentTransaction tran;
    MainFragment mainFragment;
    MyInfoFragment myInfoFragment;
    MapsFragment mapsFragment;
    ChattingFragment chattingFragment;
    RecommendFragment recommendFragment;

    private BottomNavigationView.OnNavigationItemSelectedListener mOnNavigationItemSelectedListener
            = new BottomNavigationView.OnNavigationItemSelectedListener() {

        @Override
        public boolean onNavigationItemSelected(@NonNull MenuItem item) {
            switch (item.getItemId()) {
                case R.id.navigation_home:
                    setFrag(item.getItemId());
                    return true;
                case R.id.navigation_maps:
                    setFrag(item.getItemId());
                    return true;
                case R.id.navigation_chatting:
                    setFrag(item.getItemId());
                    return true;
                case R.id.navigation_recommend:
                    setFrag(item.getItemId());
                    return true;
                case R.id.navigation_myInfo:
                    setFrag(item.getItemId());
                    return true;
            }
            return false;
        }
    };


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        BottomNavigationView navigation = (BottomNavigationView) findViewById(R.id.navigation);
        navigation.setOnNavigationItemSelectedListener(mOnNavigationItemSelectedListener);

        mainFragment = new MainFragment();
        mapsFragment = new MapsFragment();
        myInfoFragment = new MyInfoFragment();
        recommendFragment = new RecommendFragment();
        chattingFragment = new ChattingFragment();

        setFrag(R.id.navigation_home);

        ConnectThread thread = new ConnectThread("192.168.0.36");
        thread.start();
    }

    class ConnectThread extends Thread {
        String hostname;
        int port;
        Socket soc = null;
        DataOutputStream dos;
        DataInputStream dis;

        public ConnectThread(String addr) {
            hostname = addr;
            port = 10000;
        }

        public void run() {
            try {
                soc = new Socket(hostname, port);
                dos = new DataOutputStream(soc.getOutputStream());
                dis = new DataInputStream(soc.getInputStream());
            } catch (Exception e) {
                e.printStackTrace();
                Log.d("MainActivity", "정상 접속 실패");
                return;
            }

            try {
                byte[] sendMsgByte = new byte[128];
                String str = "hello python";
                String s = String.format("%-128s", str);
                sendMsgByte = s.getBytes("euc-kr");
                dos.write(sendMsgByte);
            } catch (Exception e) {

            }
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
    }


    public void setFrag(int n){    //프래그먼트를 교체하는 작업을 하는 메소드를 만들었습니다
        fm = getSupportFragmentManager();
        tran = fm.beginTransaction();
        switch (n){
            case R.id.navigation_home:
                tran.replace(R.id.frag_frame, mainFragment);
                tran.commit();
                break;
            case R.id.navigation_maps:
                tran.replace(R.id.frag_frame, mapsFragment);
                tran.commit();
                break;
            case R.id.navigation_chatting:
                tran.replace(R.id.frag_frame, chattingFragment);
                tran.commit();
                break;
            case R.id.navigation_recommend:
                tran.replace(R.id.frag_frame, recommendFragment);
                tran.commit();
                break;
            case R.id.navigation_myInfo:
                tran.replace(R.id.frag_frame, myInfoFragment);
                tran.commit();
                break;
        }

    }


}
