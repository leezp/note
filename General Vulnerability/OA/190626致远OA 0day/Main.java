package com.lee.test;

import java.io.ByteArrayOutputStream;
import java.io.UnsupportedEncodingException;

public class Main {
    String TableBase64 = "gx74KW1roM9qwzPFVOBLSlYaeyncdNbI=JfUCQRHtj2+Z05vshXi3GAEuT/m8Dpk6";

    public String DecodeBase64(String paramString)
    {
        ByteArrayOutputStream localByteArrayOutputStream = new ByteArrayOutputStream();
        String str = "";

        byte[] arrayOfByte2 = new byte[4];
        try
        {
            int j = 0;
            byte[] arrayOfByte1 = paramString.getBytes();
            while (j < arrayOfByte1.length)
            {
                for (int i = 0; i <= 3; i++)
                {
                    if (j >= arrayOfByte1.length)
                    {
                        arrayOfByte2[i] = 64;
                    }
                    else
                    {
                        int k = this.TableBase64.indexOf(arrayOfByte1[j]);
                        if (k < 0) {
                            k = 65;
                        }
                        arrayOfByte2[i] = ((byte)k);
                    }
                    j++;
                }
                localByteArrayOutputStream.write((byte)(((arrayOfByte2[0] & 0x3F) << 2) + ((arrayOfByte2[1] & 0x30) >> 4)));
                if (arrayOfByte2[2] != 64)
                {
                    localByteArrayOutputStream.write((byte)(((arrayOfByte2[1] & 0xF) << 4) + ((arrayOfByte2[2] & 0x3C) >> 2)));
                    if (arrayOfByte2[3] != 64) {
                        localByteArrayOutputStream.write((byte)(((arrayOfByte2[2] & 0x3) << 6) + (arrayOfByte2[3] & 0x3F)));
                    }
                }
            }
        }
        catch (StringIndexOutOfBoundsException localStringIndexOutOfBoundsException)
        {
            //this.FError += localStringIndexOutOfBoundsException.toString();
            System.out.println(localStringIndexOutOfBoundsException.toString());
        }
        try
        {
            str = localByteArrayOutputStream.toString("GB2312");
        }
        catch (UnsupportedEncodingException localUnsupportedEncodingException)
        {
            System.out.println(localUnsupportedEncodingException.toString());
        }
        return str;
    }

    public String EncodeBase64(String var1)
    {
        ByteArrayOutputStream var2 = new ByteArrayOutputStream();
        byte[] var7 = new byte[4];

        try {
            int var4 = 0;
            byte[] var6 = var1.getBytes("GB2312");

            while(var4 < var6.length) {
                byte var5 = var6[var4];
                ++var4;
                var7[0] = (byte)((var5 & 252) >> 2);
                var7[1] = (byte)((var5 & 3) << 4);
                if (var4 < var6.length) {
                    var5 = var6[var4];
                    ++var4;
                    var7[1] += (byte)((var5 & 240) >> 4);
                    var7[2] = (byte)((var5 & 15) << 2);
                    if (var4 < var6.length) {
                        var5 = var6[var4];
                        ++var4;
                        var7[2] = (byte)(var7[2] + ((var5 & 192) >> 6));
                        var7[3] = (byte)(var5 & 63);
                    } else {
                        var7[3] = 64;
                    }
                } else {
                    var7[2] = 64;
                    var7[3] = 64;
                }

                for(int var3 = 0; var3 <= 3; ++var3) {
                    var2.write(this.TableBase64.charAt(var7[var3]));
                }
            }
        } catch (StringIndexOutOfBoundsException var10) {
           // this.FError = this.FError + var10.toString();
            System.out.println(var10.toString());
        } catch (UnsupportedEncodingException var11) {
            System.out.println(var11.toString());
        }

        return var2.toString();

    }
    public static void main(String[] args) {

        Main m = new Main();
        //System.out.println(m.DecodeBase64("qfTdqfTdqfTdVaxJeAJQBRl3dExQyYOdNAlfeaxsdGhiyYlTcATdN1liN4KXwiVGzfT2dEg6"));
        System.out.println(m.DecodeBase64("6e4f045d4b8506bf492ada7e3390d7ce"));
        System.out.println(m.EncodeBase64("..\\..\\..\\ApacheJetspeed\\webapps\\seeyon\\test123456.jsp"));
    }
}