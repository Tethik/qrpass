package com.qrpass;

import java.util.Arrays;

import javax.crypto.SecretKey;

import android.app.Activity;
import android.app.Fragment;
import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.content.SharedPreferences.Editor;
import android.os.Bundle;
import android.util.Base64;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;

public class MainActivity extends Activity {
	private static final String TAG = "MainActivity";
	
	private QRListener currentListener = null;
	private Decrypter decrypter = new Decrypter();
	private static byte[] AESkey = null;
	
	@Override
	protected void onCreate(Bundle savedInstanceState) {
		loadAESKey();
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_main);

		if (savedInstanceState == null) {
			getFragmentManager().beginTransaction()
					.add(R.id.container, new PlaceholderFragment()).commit();
		}
	}

	@Override
	public boolean onCreateOptionsMenu(Menu menu) {

		// Inflate the menu; this adds items to the action bar if it is present.
		getMenuInflater().inflate(R.menu.main, menu);
		return true;
	}

	@Override
	public boolean onOptionsItemSelected(MenuItem item) {
		// Handle action bar item clicks here. The action bar will
		// automatically handle clicks on the Home/Up button, so long
		// as you specify a parent activity in AndroidManifest.xml.
		int id = item.getItemId();
		if (id == R.id.action_settings) {
			return true;
		}
		return super.onOptionsItemSelected(item);
	}

	/**
	 * A placeholder fragment containing a simple view.
	 */
	public static class PlaceholderFragment extends Fragment {

		public PlaceholderFragment() {
		}

		@Override
		public View onCreateView(LayoutInflater inflater, ViewGroup container,
				Bundle savedInstanceState) {
			View rootView = inflater.inflate(R.layout.fragment_main, container, false);
			return rootView;
		}
	}
	
	private void fetchQRCode() {
		Intent intent = new Intent("com.google.zxing.client.android.SCAN");
		intent.putExtra("SCAN_MODE", "QR_CODE_MODE");
		startActivityForResult(intent, 0);	
	}
	
	@Override
	public void onActivityResult(int requestCode, int resultCode, Intent data) {
		super.onActivityResult(requestCode, resultCode, data);
		if (requestCode == 0) {
			if (resultCode == Activity.RESULT_OK) {				
				String result = data.getStringExtra("SCAN_RESULT");					
				Log.i(TAG, result);
				
				if(currentListener != null)
					currentListener.QRReceived(result);
			}
		}
	}
	
	private void loadAESKey() {
		SharedPreferences sharedPref = this.getPreferences(Context.MODE_PRIVATE);
		String key = sharedPref.getString("AESKey", "");
			
		
		if(key.equals(""))  {
			Log.i(TAG, "AES key is null");
			return;
		}
		
		AESkey = Base64.decode(key, Base64.DEFAULT);
		if(AESkey.length == 32)
			Log.i(TAG, "AES key imported successfully!");
	}
	
	private void saveAESKey(String key) {
		SharedPreferences sharedPref = this.getPreferences(Context.MODE_PRIVATE);
		Editor editor = sharedPref.edit();
		AESkey = Base64.decode(key, Base64.DEFAULT);
	
		editor.putString("AESKey", key);
		editor.commit();
		
		Log.i(TAG, "" + AESkey.length);
	}
	
	public void importKey(View view) {
		currentListener = new QRListener() {			
			@Override
			public void QRReceived(String code) {
				Log.i(TAG, "import key received code");
				saveAESKey(code);
			}
		};
		
		fetchQRCode();
	}
	
	public void setText(String text) {
		TextView view = (TextView) this.findViewById(R.id.textViewStatus);
		view.setText(text);
	}
	
	public void scanPasswordCode(View view) {
		currentListener = new QRListener() {			
			@Override
			public void QRReceived(String code) {
				Log.i(TAG, "scan password received code");	
				String masterPassword = "testtest";
				byte[] data = Base64.decode(code, Base64.DEFAULT);
				
				SecretKey key = decrypter.GenerateMasterKey(masterPassword, AESkey);
				
				byte[] iv = Arrays.copyOf(data, 16);				
				byte[] ciphertext = Arrays.copyOfRange(data, 16, data.length);				
				String plain = decrypter.DecryptPassword(key, iv, ciphertext);
				setText(plain);
			}
		};
		
		fetchQRCode();
	}
	

}
