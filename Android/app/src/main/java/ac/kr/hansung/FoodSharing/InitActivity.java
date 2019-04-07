package ac.kr.hansung.FoodSharing;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;

public class InitActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_init);
    }

    @Override
    protected void onStart() {
        super.onStart();
        initApp();
    }


    private void initApp() {

        Intent intent = new Intent(this, LoginActivity.class);
        startActivityForResult(intent, 101);
    }
}
