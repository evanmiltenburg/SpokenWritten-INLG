
#__variables__

# Simple propositional conditions:
never_count = (
	'LET', 'SPEC', 'TSW', 'VZ(fin', 
	'VNW(pers,pron,nomin', 'VNW(vb,pron,stan', 
	'VNW(pers,pron,stan', 'VNW(recip,pron,dial)',
	'VNW(pers,pron,dial', 'VNW(recip,pron,obl',
	'VNW(pers,pron,obl', 'VNW(pr',	
	'VNW(aanw,pron,stan', 'VNW(refl', 
	'VNW(aanw,det,stan,nom', 'VNW(vrag', 
	'VNW(aanw,det,dat,nom', 'VNW(excl', 
	'LID(bep,stan', 'LID(onbep,stan', 
	'LID(bep,dial', 'LID(onbep,dial',
	'LID(bep,dat'	
	)

always_count = (
	'VNW(bez', 'VNW(betr', 
	'VNW(pers,pron,gen',
	'VNW(aanw,det', 'VNW(vb',
	'VNW(aanw,adv-pron',  
	'VNW(aanw,pron,gen', 'VNW(recip,pron,gen',
	'VNW(aanw,pron,dial)',
	'VZ(versm',
	'LID(bep,gen', 'LID(onbep,gen',
	'WW(vd,prenom', 'WW(vd,nom'
	)

aux = r'(^(\[ge\])?\[((zijn)|(heb)|(word)|(kan)|(moet)|(zal)|(ga(an)?)|(durf)|(mag)|(wil)|(hoef)|(b?lij[fk])|(schijn)|(dunk)|(voor\]?\[?kom))\])'
modal = r'(^(\[ge\])?\[((kan)|(moet)|(zal)|(ga(an)?)|(mag)|(wil)|(hoef)|(durf))\])'
modal_list = ('[zal]', '[moet]', '[wil]', '[kan]', '[mag]', '[durf]', '[hoef]', '[gaan]','[ga]')
copula = ('[blijf]', '[blijk]', '[lijk]', '[schijn]', '[dunk]', '[voorkom]', '[voor][kom]')
door_aan = r'\(\'(door|aan)\'\, \'VZ\(fin\)\'\, \'\[(door|aan)\]\'\)'
sec_cop = r'(^(\[ge\])?\[((b?lij[fk])|(schijn)|(dunk)|(voor\]?\[?kom))\])'
hulp = r'(^AD ((N\( )|(AD )|(LI )|(N\( VG N\( )|(VG ((AD)|(BW)) )|(SP )|(VZ )|(BW )|(VN ))*WW)'
kop = r'(^AD (LI )*(AD )*N\()'
hoe = r'\b(H|h)oe (\w+ )+((zijn)|(word))'
mod1 = r'((((V?N\(?)|(SP)|(VG)) WW)|(WW VN)|(WW LI N\()) (V?N?\(?Z?T?L?I?B?W*S?P?A?D? )+WW (VG|LE)'
mod2 = r'LE (WW) (V?N?\(?Z?T?L?I?B?W*S?P?A?D? )+WW (VG|LE)'
kop_hulp = r' te \w+n'
op = r'([Oo]p (\w+ )*l((ij)|(ee?))k(en)?t? )|(\b[Ll]((ij)|(ee?))k(en)?t? (\w+ )*op)'
licht = r'(([Ll]amp)|([Zz]onn?e?)|([Mm]aan)|((\w+)?[Ll]icht))+((je)|(en)|(straal))? '
bleek = r'(\b(([Ii]s)|([Ww]as)|([Bb]ent)|(ziet)|(werd)) (\w+ )*bleek)|([Bb]leek (\w+ )*((is)|(was)))'
kop_het = r'\b(([Bb]?[Ll]((ij)|(ee?))k)|([Ss]ch((ij)|(ee?))n))(en)?t? het (\w+ )?\W'
alsof_dat = r'\b(([Bb]?[Ll]((ij)|(ee?))k)|([Ss]ch((ij)|(ee?))n))(en)?t? (\w+ )*((alsof)|(dat))'

# List of all tags that belong to the baseline score.
baseline = ('VZ', 'WW', 'AD', 'BW', )