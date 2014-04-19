package com.qrpass;

import java.security.InvalidAlgorithmParameterException;
import java.security.InvalidKeyException;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;

import javax.crypto.BadPaddingException;
import javax.crypto.Cipher;
import javax.crypto.IllegalBlockSizeException;
import javax.crypto.NoSuchPaddingException;
import javax.crypto.SecretKey;
import javax.crypto.spec.IvParameterSpec;
import javax.crypto.spec.SecretKeySpec;

import android.util.Base64;
import android.util.Log;

public class Decrypter {
	private static final String TAG = "QRPassDecrypter";
	private static final int NUMBER_OF_ROUNDS = 10000;
	
	public SecretKey GenerateMasterKey(String masterPassword, byte[] AESKey) {
		try {
			MessageDigest sha256 = MessageDigest.getInstance("SHA-256");			
			byte[] hash = sha256.digest(masterPassword.getBytes());
			
			Cipher AES = Cipher.getInstance("AES/ECB/NoPadding");
			AES.init(Cipher.ENCRYPT_MODE, new SecretKeySpec(AESKey, "AES"));
			for(int i = 0; i < NUMBER_OF_ROUNDS; i++)	{						
				hash = AES.doFinal(hash);
			}
			
			hash = sha256.digest(hash);
			return new SecretKeySpec(hash, "AES");
		} catch (NoSuchAlgorithmException | NoSuchPaddingException | IllegalBlockSizeException | BadPaddingException e) {
			Log.e(TAG, e.toString());
		} catch (InvalidKeyException e) {
			Log.e(TAG, "Could not parse key.");
			Log.e(TAG, e.toString());			
		}
		return null;
	}
	
	public String DecryptPassword(SecretKey key, byte[] iv, byte[] ciphertext) {		
		try {
			Cipher AES = Cipher.getInstance("AES/CFB/PKCS5Padding");
			AES.init(Cipher.DECRYPT_MODE, key, new IvParameterSpec(iv));
			AES.update(ciphertext);
			byte[] plaintext = AES.doFinal();			
			StringBuilder builder = new StringBuilder();
			for(byte b : plaintext)
				builder.append((char) b);
			return builder.toString();
		} catch (InvalidKeyException | NoSuchAlgorithmException | NoSuchPaddingException | IllegalBlockSizeException | BadPaddingException | InvalidAlgorithmParameterException e) {
			Log.e(TAG, "Failed to decrypt");
			Log.e(TAG, e.toString());	
		}
		
		return "";
	}
}
