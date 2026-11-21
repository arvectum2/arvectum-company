using System;
using System.Text;
using System.Collections.Generic;
using System.Runtime.InteropServices;
using System.Drawing;
using System.Drawing.Imaging;

public static class PrivateGdiProbe
{
    [DllImport("gdi32.dll", EntryPoint="AddFontResourceExW", CharSet=CharSet.Unicode)]
    static extern int AddFont(string filename, uint flags, IntPtr reserved);
    [DllImport("gdi32.dll", EntryPoint="RemoveFontResourceExW", CharSet=CharSet.Unicode)]
    static extern bool RemoveFont(string filename, uint flags, IntPtr reserved);
    [DllImport("gdi32.dll", EntryPoint="CreateFontW", CharSet=CharSet.Unicode)]
    static extern IntPtr CreateFont(int height, int width, int escapement, int orientation,
       int weight, int italic, int underline, int strikeout, int charset, int output,
       int clipping, int quality, int family, string face);
    [DllImport("gdi32.dll")] static extern IntPtr SelectObject(IntPtr dc, IntPtr obj);
    [DllImport("gdi32.dll")] static extern bool DeleteObject(IntPtr obj);
    [DllImport("gdi32.dll", EntryPoint="GetTextFaceW", CharSet=CharSet.Unicode)]
    static extern int GetTextFace(IntPtr dc, int capacity, StringBuilder value);
    [DllImport("gdi32.dll", EntryPoint="GetTextMetricsW", CharSet=CharSet.Unicode)]
    static extern bool GetTextMetrics(IntPtr dc, out TEXTMETRIC tm);
    [DllImport("gdi32.dll", EntryPoint="TextOutW", CharSet=CharSet.Unicode)]
    static extern bool TextOut(IntPtr dc, int x, int y, string text, int count);
    [DllImport("gdi32.dll")] static extern int SetBkMode(IntPtr dc, int mode);
    [DllImport("gdi32.dll")] static extern int SetTextColor(IntPtr dc, int color);
    [StructLayout(LayoutKind.Sequential)]
    public struct TEXTMETRIC {
      public int height, ascent, descent, internalLeading, externalLeading;
      public int aveCharWidth, maxCharWidth, weight, overhang, aspectX, aspectY;
      public ushort firstChar, lastChar, defaultChar, breakChar;
      public byte italic, underlined, struckOut, pitchFamily, charset;
    }
    public static Dictionary<string,object> Probe(string file,string family,string output)
    {
      var result=new Dictionary<string,object>();
      result["family"]=family; result["family_length"]=family.Length;
      result["gdi_limit"]=31; result["gdi_exact_family"]=false;
      int count=AddFont(file,0x10,IntPtr.Zero); // process-private only, no registry.
      result["registered"]=count>0;
      if(count<=0) {result["diagnostic"]="Private registration failed (CFF unsupported?)";return result;}
      try {
        string requested=family.Length>31?family.Substring(0,31):family;
        result["passed_to_CreateFont"]=requested;
        IntPtr font=CreateFont(-40,0,0,0,400,0,0,0,1,0,0,0,0,requested);
        if(font==IntPtr.Zero) {result["diagnostic"]="CreateFont failed";return result;}
        try {
          using(var bitmap=new Bitmap(1200,150))
          using(var graphics=Graphics.FromImage(bitmap)) {
            graphics.Clear(Color.White);
            IntPtr dc=graphics.GetHdc();
            try {
              IntPtr old=SelectObject(dc,font);
              try {
                var name=new StringBuilder(128);
                GetTextFace(dc,name.Capacity,name);
                string actual=name.ToString();
                result["actual_face"]=actual;
                result["gdi_exact_family"]=string.Equals(actual,family,StringComparison.OrdinalIgnoreCase);
                TEXTMETRIC tm;
                if(GetTextMetrics(dc,out tm)) {
                  result["tmHeight"]=tm.height;result["tmAscent"]=tm.ascent;
                  result["tmDescent"]=tm.descent;result["tmExternalLeading"]=tm.externalLeading;
                }
                SetBkMode(dc,1);SetTextColor(dc,0x00320000);
                string sample="AV To Арвектум 1 250 000 ₽";
                TextOut(dc,20,20,sample,sample.Length);
              } finally {SelectObject(dc,old);}
            } finally {graphics.ReleaseHdc(dc);}
            bitmap.Save(output,ImageFormat.Png);
          }
        } finally {DeleteObject(font);}
      } finally {RemoveFont(file,0x10,IntPtr.Zero);}
      return result;
    }
}
