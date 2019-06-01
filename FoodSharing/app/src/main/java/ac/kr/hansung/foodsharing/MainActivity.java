package ac.kr.hansung.foodsharing;

import android.content.Intent;
import android.os.Bundle;
import android.support.design.widget.BottomNavigationView;
import android.support.v4.app.FragmentManager;
import android.support.v4.app.FragmentTransaction;
import android.support.v7.app.AppCompatActivity;
import android.support.annotation.NonNull;
import android.view.MenuItem;

public class MainActivity extends AppCompatActivity {
    MainFragment mainFragment;
    ChatFragment chatFragment;
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
                case R.id.navigation_chat:
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
        chatFragment = new ChatFragment();

        Intent myIntent = new Intent(this, SocketService.class);
        myIntent.putExtra("command","1");
        startService(myIntent);
        startService(myIntent);

        setFrag(R.id.navigation_home);
    }

    public void setFrag(int n){    //프래그먼트를 교체하는 작업을 하는 메소드를 만들었습니다
        fm = getSupportFragmentManager();
        tran = fm.beginTransaction();
        switch (n){
            case R.id.navigation_home:
                tran.replace(R.id.frag_frame, mainFragment);
                tran.commit();
                break;
            case R.id.navigation_chat:
                tran.replace(R.id.frag_frame, chatFragment);
                tran.commit();
                break;
        }

    }

}
