#!/usr/bin/env python3
import os as _o,sys as _s,glob as _g,platform as _p
from hashlib import md5 as _h5
from base64 import b64encode as _be,b64decode as _bd
try:
 import readline as _rl;_R=True
except ImportError:_R=False
_=16
_Z=bytes
_Y=bytearray
_X=list
_W=range
_V=len
_U=isinstance
_T=input
_Q=print
_J=tuple
_N=type(None)
_0x=(0x63,0x7C,0x77,0x7B,0xF2,0x6B,0x6F,0xC5,0x30,0x01,0x67,0x2B,0xFE,0xD7,0xAB,0x76,0xCA,0x82,0xC9,0x7D,0xFA,0x59,0x47,0xF0,0xAD,0xD4,0xA2,0xAF,0x9C,0xA4,0x72,0xC0,0xB7,0xFD,0x93,0x26,0x36,0x3F,0xF7,0xCC,0x34,0xA5,0xE5,0xF1,0x71,0xD8,0x31,0x15,0x04,0xC7,0x23,0xC3,0x18,0x96,0x05,0x9A,0x07,0x12,0x80,0xE2,0xEB,0x27,0xB2,0x75,0x09,0x83,0x2C,0x1A,0x1B,0x6E,0x5A,0xA0,0x52,0x3B,0xD6,0xB3,0x29,0xE3,0x2F,0x84,0x53,0xD1,0x00,0xED,0x20,0xFC,0xB1,0x5B,0x6A,0xCB,0xBE,0x39,0x4A,0x4C,0x58,0xCF,0xD0,0xEF,0xAA,0xFB,0x43,0x4D,0x33,0x85,0x45,0xF9,0x02,0x7F,0x50,0x3C,0x9F,0xA8,0x51,0xA3,0x40,0x8F,0x92,0x9D,0x38,0xF5,0xBC,0xB6,0xDA,0x21,0x10,0xFF,0xF3,0xD2,0xCD,0x0C,0x13,0xEC,0x5F,0x97,0x44,0x17,0xC4,0xA7,0x7E,0x3D,0x64,0x5D,0x19,0x73,0x60,0x81,0x4F,0xDC,0x22,0x2A,0x90,0x88,0x46,0xEE,0xB8,0x14,0xDE,0x5E,0x0B,0xDB,0xE0,0x32,0x3A,0x0A,0x49,0x06,0x24,0x5C,0xC2,0xD3,0xAC,0x62,0x91,0x95,0xE4,0x79,0xE7,0xC8,0x37,0x6D,0x8D,0xD5,0x4E,0xA9,0x6C,0x56,0xF4,0xEA,0x65,0x7A,0xAE,0x08,0xBA,0x78,0x25,0x2E,0x1C,0xA6,0xB4,0xC6,0xE8,0xDD,0x74,0x1F,0x4B,0xBD,0x8B,0x8A,0x70,0x3E,0xB5,0x66,0x48,0x03,0xF6,0x0E,0x61,0x35,0x57,0xB9,0x86,0xC1,0x1D,0x9E,0xE1,0xF8,0x98,0x11,0x69,0xD9,0x8E,0x94,0x9B,0x1E,0x87,0xE9,0xCE,0x55,0x28,0xDF,0x8C,0xA1,0x89,0x0D,0xBF,0xE6,0x42,0x68,0x41,0x99,0x2D,0x0F,0xB0,0x54,0xBB,0x16)
_1x=[0]*256
for _i2,_v2 in enumerate(_0x):_1x[_v2]=_i2
_1x=_J(_1x)
_2x=(0x01,0x02,0x04,0x08,0x10,0x20,0x40,0x80,0x1B,0x36)
BLOCK_SIZE=_
def _a3(a):return((a<<1)^0x11B)&0xFF if a&0x80 else(a<<1)&0xFF
def _b4(a,b):
 r=0
 for _k in _W(8):
  if b&1:r^=a
  a=_a3(a);b>>=1
 return r
def _c5(s):return[_0x[b]for b in s]
def _d6(s):return[_1x[b]for b in s]
def _e7(s):
 q=s[:];q[1],q[5],q[9],q[13]=q[5],q[9],q[13],q[1];q[2],q[6],q[10],q[14]=q[10],q[14],q[2],q[6];q[3],q[7],q[11],q[15]=q[15],q[3],q[7],q[11]
 return q
def _f8(s):
 q=s[:];q[1],q[5],q[9],q[13]=q[13],q[1],q[5],q[9];q[2],q[6],q[10],q[14]=q[10],q[14],q[2],q[6];q[3],q[7],q[11],q[15]=q[7],q[11],q[15],q[3]
 return q
def _g9(s):
 q=s[:]
 for c in _W(4):
  i=c*4;a=q[i:i+4];q[i]=_b4(a[0],2)^_b4(a[1],3)^a[2]^a[3];q[i+1]=a[0]^_b4(a[1],2)^_b4(a[2],3)^a[3];q[i+2]=a[0]^a[1]^_b4(a[2],2)^_b4(a[3],3);q[i+3]=_b4(a[0],3)^a[1]^a[2]^_b4(a[3],2)
 return q
def _hA(s):
 q=s[:]
 for c in _W(4):
  i=c*4;a=q[i:i+4];q[i]=_b4(a[0],14)^_b4(a[1],11)^_b4(a[2],13)^_b4(a[3],9);q[i+1]=_b4(a[0],9)^_b4(a[1],14)^_b4(a[2],11)^_b4(a[3],13);q[i+2]=_b4(a[0],13)^_b4(a[1],9)^_b4(a[2],14)^_b4(a[3],11);q[i+3]=_b4(a[0],11)^_b4(a[1],13)^_b4(a[2],9)^_b4(a[3],14)
 return q
def _iB(s,k):return[a^b for a,b in zip(s,k)]
def _jC(k):
 n,m=4,10;w=[_X(k[4*i:4*i+4])for i in _W(n)]
 for i in _W(n,4*(m+1)):
  t=w[i-1][:];
  if i%n==0:t=[_0x[b]for b in t[1:]+t[:1]];t[0]^=_2x[i//n-1]
  w.append([a^b for a,b in zip(w[i-n],t)])
 return[sum((w[r*4+c]for c in _W(4)),[])for r in _W(m+1)]
def _kD(bl,rk):
 st=_iB(_X(bl),rk[0])
 for r in _W(1,10):st=_iB(_g9(_e7(_c5(st))),rk[r])
 return _Z(_iB(_e7(_c5(st)),rk[10]))
def _lE(bl,rk):
 st=_iB(_X(bl),rk[10])
 for r in _W(9,0,-1):st=_hA(_iB(_d6(_f8(st)),rk[r]))
 return _Z(_iB(_d6(_f8(st)),rk[0]))
def pkcs7_pad(d,bs=_):
 pl=bs-(_V(d)%bs);return d+_Z([pl]*pl)
def pkcs7_unpad(d,bs=_):
 if not d:raise ValueError(_Z.fromhex('43616e6e6f7420756e70616420656d7074792064617461').decode())
 pl=d[-1]
 if pl<1 or pl>bs:raise ValueError(f"{_Z.fromhex('496e76616c69642070616464696e67206c656e6774683a20').decode()}{pl}")
 if d[-pl:]!=_Z([pl]*pl):raise ValueError(_Z.fromhex('496e76616c696420504b43533720706164').decode()+_Z.fromhex('64696e67').decode())
 return d[:-pl]
class AESCipher:
 __slots__=('\x6b\x65\x79','_rk')
 def __init__(self,k):
  if not k:raise ValueError(_Z.fromhex('4b6579206d757374206e6f7420626520656d707479').decode())
  self.key=_h5((k.encode('\x75\x74\x66\x2d\x38')if _U(k,str)else k)).digest();self._rk=_jC(self.key)
 def encrypt(self,d):
  d=d.encode('\x75\x74\x66\x2d\x38')if _U(d,str)else d
  if not _U(d,(_Z,_Y)):raise TypeError(_Z.fromhex('44617461206d75737420626520').decode()+'\x73\x74\x72\x2c\x20\x62\x79\x74\x65\x73\x2c\x20\x6f\x72\x20\x62\x79\x74\x65\x61\x72\x72\x61\x79')
  iv=_o.urandom(_);pd=pkcs7_pad(d);ct=_Y();pv=iv
  for i in _W(0,_V(pd),_):
   bk=pd[i:i+_];xr=_Z(a^b for a,b in zip(bk,pv));ec=_kD(xr,self._rk);ct.extend(ec);pv=ec
  return _be(iv+_Z(ct))
 def decrypt(self,d):
  d=d.encode('\x75\x74\x66\x2d\x38')if _U(d,str)else d
  if not _U(d,(_Z,_Y)):raise TypeError(_Z.fromhex('44617461206d75737420626520').decode()+'\x73\x74\x72\x2c\x20\x62\x79\x74\x65\x73\x2c\x20\x6f\x72\x20\x62\x79\x74\x65\x61\x72\x72\x61\x79')
  rw=_bd(d)
  if _V(rw)<_*2:raise ValueError(_Z.fromhex('43697068657274657874').decode()+_Z.fromhex('20746f6f2073686f727420286d75737420636f6e7461696e204956202b206174206c65617374206f6e6520626c6f636b29').decode())
  if _V(rw)%_!=0:raise ValueError(_Z.fromhex('43697068657274657874206c656e677468206973206e6f742061206d756c7469706c65206f6620626c6f636b2073697a65').decode())
  iv=rw[:_];ct=rw[_:];pt=_Y();pv=iv
  for i in _W(0,_V(ct),_):
   bk=ct[i:i+_];dc=_lE(bk,self._rk);pt.extend(_Z(a^b for a,b in zip(dc,pv)));pv=bk
  return pkcs7_unpad(_Z(pt))
class _mF:
 def __init__(self):self._q=[]
 def complete(self,t,st):
  if st==0:self._q=[m+_o.sep if _o.path.isdir(m)else m for m in _g.glob(_o.path.expanduser(t)+'*')]
  return self._q[st]if st<_V(self._q)else None
def _nG(pr):
 if not _R:return _T(pr).strip()
 fc=_mF();oc=_rl.get_completer();od=_rl.get_completer_delims()
 try:
  _rl.set_completer(fc.complete);_rl.set_completer_delims(' \t\n;')
  _rl.parse_and_bind('bind ^I rl_complete'if(getattr(_rl,'\x5f\x5f\x64\x6f\x63\x5f\x5f','')or'')and'\x6c\x69\x62\x65\x64\x69\x74'in _rl.__doc__ else'tab: complete')
  return _T(pr).strip()
 finally:_rl.set_completer(oc);_rl.set_completer_delims(od)
def _oH(fp):
 try:
  ln=_o.path.getsize(fp)
  with open(fp,'\x72\x2b\x62')as f:f.write(_o.urandom(ln));f.flush();_o.fsync(f.fileno())
  _o.remove(fp)
 except OSError:_o.remove(fp)
def _pH():return'\x5c'if _p.system()=='\x57\x69\x6e\x64\x6f\x77\x73'else'\x2f'
def _qI(ci,d,fn,td):
 ec=ci.encrypt(d);_Q('\x3d'*10+'\x20\x52\x45\x53\x55\x4c\x54\x20'+'\x3d'*10)
 if td=='\x66':
  on=fn+'\x2e\x61\x65\x73'
  with open(on,'\x77\x62')as f:f.write(ec)
  _oH(fn);sp=_pH();_Q(f'\x5b\x2b\x5d\x20\x45\x6e\x63\x72\x79\x70\x74\x65\x64\x20\x64\x61\x74\x61\x20\x73\x61\x76\x65\x64\x20\x74\x6f\x20{_o.getcwd()}{sp}{on}');_Q(f'\x5b\x2b\x5d\x20\x4f\x72\x69\x67\x69\x6e\x61\x6c\x20\x66\x69\x6c\x65\x20\x73\x65\x63\x75\x72\x65\x6c\x79\x20\x64\x65\x6c\x65\x74\x65\x64\x3a\x20{fn}')
 else:
  _ec=ec.decode('utf-8');_Q(f'\x5b\x2b\x5d\x20\x45\x6e\x63\x72\x79\x70\x74\x65\x64\x20\x64\x61\x74\x61\x3a\x20{_ec}')
def _rJ(ci,d,fn,td):
 pt=ci.decrypt(d);_Q('\x3d'*10+'\x20\x52\x45\x53\x55\x4c\x54\x20'+'\x3d'*10)
 if td=='\x66':
  on=fn.replace('\x2e\x61\x65\x73','')if fn.endswith('\x2e\x61\x65\x73')else fn+'\x2e\x64\x65\x63'
  with open(on,'\x77\x62')as f:f.write(pt)
  _oH(fn);sp=_pH();_Q(f'\x5b\x2b\x5d\x20\x44\x65\x63\x72\x79\x70\x74\x65\x64\x20\x64\x61\x74\x61\x20\x73\x61\x76\x65\x64\x20\x74\x6f\x20{_o.getcwd()}{sp}{on}')
 else:
  _pt=pt.decode('utf-8');_Q(f'\x5b\x2b\x5d\x20\x44\x65\x63\x72\x79\x70\x74\x65\x64\x20\x64\x61\x74\x61\x3a\x20{_pt}')
def _sK():
 md=_T(_Z.fromhex('5b2a5d2043686f6f7365206d6f646520652f642028656e63727970742f646563727970 74293a20'.replace(' ','')).decode()).strip().lower()
 if md not in('\x65','\x64'):_s.exit(_Z.fromhex('5b2d5d20496e76616c6964206d6f64652e205573652022652220666f7220656e6372797074206f72202264222066 6f72206465637279 70742e'.replace(' ','')).decode())
 td=_T(_Z.fromhex('5b2a5d2043686f6f7365206461746120747970 6520662f732028 66696c652f737472696e67293a20'.replace(' ','')).decode()).strip().lower();fn=''
 if td=='\x66':
  fn=_nG(_Z.fromhex('5b2a5d20496e7075742066696c65206e616d653a20').decode())
  if not fn:_s.exit(_Z.fromhex('5b2d5d2046696c65206e616d652063616e6e6f7420626520656d7074792e').decode())
  if not _o.path.isfile(fn):_s.exit(f"{_Z.fromhex('5b2d5d2043616e6e6f742066696e642066696c653a20').decode()}{fn}")
  with open(fn,'\x72\x62')as f:d=f.read()
 elif td=='\x73':
  d=_T(_Z.fromhex('5b2a5d20496e70757420746865206461 74613a20'.replace(' ','')).decode()).encode('\x75\x74\x66\x2d\x38')
  if not d:_s.exit(_Z.fromhex('5b2d5d204461746120 63616e6e6f74206265 20656d7074792e'.replace(' ','')).decode())
 else:_s.exit(_Z.fromhex('5b2d5d20496e76616c696420747970652e20557365202266222066 6f722066696c65206f72202273222066 6f7220737472696e672e'.replace(' ','')).decode())
 ak=_T(_Z.fromhex('5b2a5d20456e746572207365637572697479206b65793a20').decode())
 if not ak:_s.exit(_Z.fromhex('5b2d5d20536563757269747920 6b65792063616e6e6f7420626520656d7074792e'.replace(' ','')).decode())
 return md,d,ak,fn,td
if __name__=='\x5f\x5f\x6d\x61\x69\x6e\x5f\x5f':
 try:
  md,d,ak,fn,td=_sK();ci=AESCipher(ak)
  {'\x65':_qI,'\x64':_rJ}[md](ci,d,fn,td)
 except KeyboardInterrupt:_Q(_Z.fromhex('0a5b215d20496e7465727275707465642062 7920757365722e'.replace(' ','')).decode());_s.exit(130)
 except(ValueError,TypeError)as e:_s.exit(f"{_Z.fromhex('5b2d5d204f7065726174696f6e206661696c65643a20').decode()}{e}")
 except Exception:_s.exit(_Z.fromhex('5b2d5d2057726f6e67206b6579206f7220636f72727570746564206461 74612e204f7065726174696f6e206661696c65642e'.replace(' ','')).decode())
