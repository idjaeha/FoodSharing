package ac.kr.hansung.foodsharing;


import android.content.Intent;
import android.os.Bundle;
import android.support.design.widget.BottomNavigationView;
import android.support.v4.app.FragmentManager;
import android.support.v4.app.FragmentTransaction;
import android.support.v7.app.AppCompatActivity;
import android.support.annotation.NonNull;
import android.util.Log;
import android.view.MenuItem;

import static ac.kr.hansung.foodsharing.InitActivity.mobileInfo;


public class MainActivity extends AppCompatActivity {
    MainFragment mainFragment;
    RecommendFragment recommendFragment;
    InfoFragment infoFragment;
    FragmentManager fm;
    FragmentTransaction tran;

    private BottomNavigationView.OnNavigationItemSelectedListener mOnNavigationItemSelectedListener
            = new BottomNavigationView.OnNavigationItemSelectedListener() {

        @Override
        public boolean onNavigationItemSelected(@NonNull MenuItem item) {
            switch (item.getItemId()) {
                case R.id.navigation_home:
                    setFrag(item.getItemId());
                    return true;
                case R.id.navigation_recommend:
                    setFrag(item.getItemId());
                    return true;
                case R.id.navigation_info:
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

        BottomNavigationView navView = findViewById(R.id.nav_view);
        navView.setOnNavigationItemSelectedListener(mOnNavigationItemSelectedListener);

        mainFragment = new MainFragment();
        recommendFragment = new RecommendFragment();
        infoFragment = new InfoFragment();

        Log.d("MainActivity", "유저 번호 : " + mobileInfo.getUserNum());
        Log.d("MainActivity", "아이디 : " + mobileInfo.getId());
        Log.d("MainActivity", "패스워드 : " + mobileInfo.getPwd());

        setFrag(R.id.navigation_home);
    }

    @Override
    protected void onStop() {
        super.onStop();
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();
        Intent logoutIntent = new Intent(this, SocketService.class);
        logoutIntent.putExtra("command", "20");
        logoutIntent.putExtra("user_num", mobileInfo.userNum);
        startService(logoutIntent);
    }

    public void setFrag(int n){    //프래그먼트를 교체하는 작업을 하는 메소드를 만들었습니다
        fm = getSupportFragmentManager();
        tran = fm.beginTransaction();
        switch (n){
            case R.id.navigation_home:
                tran.replace(R.id.frag_frame, mainFragment);
                tran.commit();
                break;
            case R.id.navigation_recommend:
                tran.replace(R.id.frag_frame, recommendFragment);
                tran.commit();
                break;
            case R.id.navigation_info:
                tran.replace(R.id.frag_frame, infoFragment);
                tran.commit();
                break;
        }

    }

}
