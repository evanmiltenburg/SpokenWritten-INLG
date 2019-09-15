#!/usr/bin/python

import nltk
import re
import numpy as np
import glob
import json

from __variables__ import (never_count, always_count, aux, modal,
							modal_list, copula, door_aan, sec_cop,
							hulp, kop, hoe, mod1, mod2, kop_hulp, op,
							licht, bleek, kop_het, alsof_dat, baseline)
from prep import prepare_data


def Dutch_idea_density(inputfile, output='PID'):
	"""
	This functions takes as input a Frog-file.
	The propositional idea density and baseline score are based upon
	the POS-tag of each word.
	All words that meet the baseline or propositional conditions are counted.
	By default, the function returns the propositional density of the textfile.
	"""

	text = prepare_data(inputfile)
	result_dict = {'overall': 0, 'per_sentence': []}

	# Initiate counts.
	wordcount = 0
	baseline_count = 0
	total_baseline = 0
	count = 0
	total_propcount = 0
	total_wordcount = 0

	for sent_id, sentence in enumerate(text):
		# The amount of words is limited to the smallest text.
		if wordcount < 12030:

			# Word count and baseline count.
			for word in sentence:
				if word[1] != 'LET()':
					# Count each token, except punctuation.
					wordcount += 1
				if word[1][:2] in baseline:
					# Count all tags that are part of the Baseline list.
					baseline_count += 1

			# Create sentence string of all tokens.
			sent = [word[0] for word in sentence]
			remove1 = re.compile(r"([\"\']\, [\"\'])|(\[[\"\'])|([\'\"]\])")
			sent_without = remove1.sub(" ", str(sent))

			# Create tag string of the 2 first characters of each tag.
			tag = [word[1][:2] for word in sentence]
			tag_without = remove1.sub(" ", str(tag))

			# Define the value of each token variable (when present).
			# & Create a string of all preceding tags
			# and a string of all following tags and tokens.
			for i in range(0, len(sentence)):
				vari_last = sentence[-2]
				try:
					vari_min4 = sentence[i - 4]
					tag_prev = str(vari_min4[1][:2])
				except IndexError:
					tag_prev = str(0)
					pass
				try:
					vari_min3 = sentence[i - 3]
					tag_prev = str(tag_prev + ' ' + vari_min3[1][:2])
				except IndexError:
					pass
				try:
					vari_min2 = sentence[i - 2]
					tag_prev = str(tag_prev + ' ' + vari_min2[1][:2])
				except IndexError:
					pass
				vari_min1 = sentence[i - 1]
				tag_prev = str(tag_prev + ' ' + vari_min1[1][:2])
				vari = sentence[i]
				try:
					vari1 = sentence[i + 1]
					sent_next = str(vari1[0])
					tag_next = str(vari1[1][:2])
				except IndexError:
					pass
				try:
					vari2 = sentence[i + 2]
					sent_next = str(sent_next + ' ' + vari2[0])
					tag_next = str(tag_next + ' ' + vari2[1][:2])
				except IndexError:
					pass
				try:
					vari3 = sentence[i + 3]
					sent_next = str(sent_next + ' ' + vari3[0])
					tag_next = str(tag_next + ' ' + vari3[1][:2])
				except IndexError:
					pass
				try:
					vari4 = sentence[i + 4]
					sent_next = str(sent_next + ' ' + vari4[0])
					tag_next = str(tag_next + ' ' + vari4[1][:2])
				except IndexError:
					pass
				try:
					vari5 = sentence[i + 5]
					sent_next = str(sent_next + ' ' + vari5[0])
					tag_next = str(tag_next + ' ' + vari5[1][:2])
				except IndexError:
					pass
				try:
					vari6 = sentence[i + 6]
					sent_next = str(sent_next + ' ' + vari6[0])
					tag_next = str(tag_next + ' ' + vari6[1][:2])
				except IndexError:
					pass
				try:
					vari7 = sentence[i + 7]
					sent_next = str(sent_next + ' ' + vari7[0])
					tag_next = str(tag_next + ' ' + vari7[1][:2])
				except IndexError:
					pass
				try:
					vari8 = sentence[i + 8]
					sent_next = str(sent_next + ' ' + vari8[0])
					tag_next = str(tag_next + ' ' + vari8[1][:2])
				except IndexError:
					pass
				try:
					vari9 = sentence[i + 9]
					sent_next = str(sent_next + ' ' + vari9[0])
					tag_next = str(tag_next + ' ' + vari9[1][:2])
				except IndexError:
					pass
				try:
					vari10 = sentence[i + 10]
					sent_next = str(sent_next + ' ' + vari10[0])
					tag_next = str(tag_next + ' ' + vari10[1][:2])
				except IndexError:
					pass
				try:
					vari11 = sentence[i + 11]
					sent_next = str(sent_next + ' ' + vari11[0])
					tag_next = str(tag_next + ' ' + vari11[1][:2])
				except IndexError:
					pass

				# Count propositions.
				# Simple proposition count: always/never.
				if vari[1].startswith(never_count):
					continue
				elif vari[1].startswith(always_count):
					# Never count existential 'Er'.
					if vari[0] not in ('er', 'Er'):
						count += 1

				# Proposition count restriction rules:
				elif vari[1][:1] == 'N':
					if vari[1].endswith('gen)'):  # Only count [noun]+'s.
						if not vari_min1[0] in ("'s", 'des'):
							count += 1

				elif vari[1][:2] == 'AD':
					if not vari[1].startswith('ADJ(nom'):
						# Never count nominative adjectives.
						count += 1

				elif vari[1][:2] == 'TW':
					if not re.search(r'TW\(((hoofd)|(rang)),nom', vari[1]):
						# Never count nominative numerals.
						count += 1

				elif vari[1].startswith('VNW(onbep,pron,stan'):
					if vari[0] == 'wat':
						# Only count 'wat'.
						count += 1

				elif vari[1].startswith('VNW(onbep'):
					if vari[0] in ('Geen', 'geen'):
						if not re.search(r'\[Gg]een .* tenzij ', sent_without):
							# 'Geen ... tenzij' is one proposition, only count 'tenzij'.
							count += 1
					elif vari[0] == 'enkele':
						if not re.search(r'\b[Gg]een enkele ', sent_without):
							# 'Geen ... enkele' is one proposition, only count 'geen'.
							count += 1
					elif vari[0] == 'meer':
						if not re.search(r'\b[Gg]een (\w+ )*meer', sent_without):
							# 'Geen ... meer' is one proposition, only count 'geen'.
							count += 1
					else:
						count += 1

				# Empty expression, preceding verbs (~'to'[+verb]).
				elif vari[1] == 'VZ(init)':
					if vari[0] in ('Te', 'te'):
						if vari1[1][:2] != 'WW':
							# Never count 'te' [+ WW].
							count += 1
					elif vari[0] in ('Om', 'om'):
						if not re.search(r'\bom (\w+ )*te ', sent_without):
							# Never count 'om' [+ 'te' WW].
							count += 1
					elif vari[0] in ('Aan', 'aan'):
						if not ((vari1[0] == 'het' or vari1[0] == "'t") and
								vari2[1][:2] == 'WW'):
							# Never count 'aan' [+ 'het' WW].
							count += 1
					else:
						count += 1

				# Wordcombinations that count as 1 proposition:
				elif vari[1] == 'BW()':
					if vari[0] in ('zowel', 'Zowel'):
						if not re.search(r'\b[Zz]owel .* als ', sent_without):
							# 'Zowel ... als' is one proposition, only count 'als'.
							count += 1
					elif vari[0] in ('nog', 'Nog'):
						if not re.search(r'\b[Nn]og nooit', sent_without):
							# 'Nog nooit' is one proposition, only count 'nooit'.
							count += 1
					elif vari[0] == 'niet':
						if not re.search(r'\bniet.*((meer)|([Tt]enzij))', sent_without):
							# 'Niet ... meer/tenzij' is one proposition, only count 'meer'/'tenzij'.
							count += 1
					elif vari[0] in ('ook', 'Ook'):
						if not vari1[0] == 'al':
							# 'Ook al' is one proposition, only count 'al'.
							count += 1
					else:
						count += 1

				elif vari[1][:2] == 'VG':
					if vari[0] == 'dan':
						if not re.search(r'\b(([Mm]eer)|([Aa]ls)).*dan ', sent_without):
							# 'Meer/Als ... dan' is one proposition, only count 'Meer'/'Als'.
							count += 1
					else:
						count += 1

				elif vari[1].startswith('WW'):

					# Auxiliary verbs: modal verbs and copula verbs.
					if re.search(aux, vari[2]):

						# 'Hebben'
                        # Always count lexical verb.
                        # Never count all other instances.
						if re.search(r'\[heb\]', vari[2]):
							if (vari_min2[0] == 'te' and vari_min1[1][:4] == 'WW(i'):
								continue  # Never count.
							elif (vari_min2[1][:4] == 'WW(i'and vari_min1[0] == 'te'):
								continue  # Never count.
							elif vari[0] == 'gehad':
								if vari1[1][:4] != 'WW(i':
									# 'Gehad' always functions as lexical verb.
									count += 1
							else:
								if not (vari_min1[1][:4] == 'WW(v' or vari1[1][:4] == 'WW(v'):
									if not (vari_min2[1][:4] == 'WW(v' and vari_min1[1][:2] not in ('VG', 'LE')):
										if (vari1[0] == ',' or vari1[1][:2] == 'VG'):
											count += 1  # Lexical verb.
										else:
											if not re.search(r'WW ((VZ|LI|N\(|VN|SP|TW|AD|BW) )*WW', tag_without):
												# When only verb in sentence: lexical verb.
												count += 1
											elif not (re.search(r'\[heb\].*WW\((vd|inf)\,vrij', str(sentence)) or
													  re.search(r'WW\((vd|inf)\,vrij.*\[heb\]', str(sentence))):
												if (re.search(r'\[heb\].*VZ\(fin\)', str(sentence)) or
														re.search(r'VZ\(fin\).*\[heb\]', str(sentence))):
													if (re.search(door_aan, str(vari1)) or re.search(door_aan, str(vari2)) or
															re.search(door_aan, str(vari3)) or re.search(door_aan, str(vari4))):
														# Always count lexical verb with fixed preposition.
														count += 1
												else:
													# When other verb functions as ADJ: Lexical verb.
													count += 1
											else:
												if vari_min1[2].startswith(modal_list):
													# When preceded by modal verb: Lexical verb.
													count += 1

						# 'Zijn' & 'Worden':
						# Always count copula verb, accompanied by Noun phrase.
						# Never count all other instances.
						elif re.search(r'word', vari[2]) or re.search(r'zijn', vari[2]):
							if (vari_min2[0] == 'te' and vari_min1[1][:4] == 'WW(i'):
								continue  # Never count.
							elif (vari_min2[1][:4] in ('WW(v', 'ADJ(') and vari_min1[0] == 'te'):
								continue  # Never count.
							elif not (re.search(r'(\w+ )*aan het ', sent_next) and
									  re.search(r'VZ LI WW', tag_next)):
								if vari_min1[1][:10] != 'WW(vd,vrij' and vari1[1][:10] != 'WW(vd,vrij':
									if not re.search(r'ADJ\([vp]', vari_min1[1][:5]):
										if vari_last != vari:
											if vari1[1][:3] == 'ADJ':
												if vari2[1] != 'LET()':
													if not re.search(hulp, tag_next):
														if re.search(kop, tag_next):
															count += 1
											else:
												if re.search(aux, vari_min1[2]):
													if vari1[1][:4] != 'WW(v':
														if not re.search(hoe, sent_without):
															if (vari_min2[1][:1] == 'N' or vari_min2[1][:5] == 'ADJ(n'):
																if not vari_min3[1][:2] == 'VZ':
																	count += 1
															elif vari_min2[1][:5] not in ('ADJ(v', 'ADJ(p', 'WW(vd'):
																if (vari_min3[1][:1] == 'N' or vari_min3[1][:5] == 'ADJ(n'):
																	count += 1
												elif not vari1[1][:2] == 'VZ':
													if (vari_min1[1][:2] == 'VZ' and vari[1][:4] == 'WW(i'):
														if (vari_min2[1][:1] == 'N' or vari_min2[1][:5] == 'ADJ(n'):
															count += 1
													else:
														if vari1[1] == 'LET()':
															if (vari_min1[1][:1] in ('N', 'S') or vari_min1[1][:5] == 'ADJ(n'):
																if not (vari_min2[1][:2] == 'VZ' or
																		(vari_min3[1][:2] == 'VZ' and vari_min2[1][:2] in ('LI', 'VN'))):
																	count += 1
														elif vari_min1[1][:3] == 'VNW':
															if (vari1[1][:2] in ('N(', 'LI', 'SP', 'VN') and vari3[1][:4] != 'WW(v'):
																count += 1
															elif (vari2[1][:2] in ('N(', 'SP') and
																	vari3[1][:4] != 'WW(v' and vari4[1][:4] != 'WW(v'):
																count += 1
															elif (vari1[1][:2] == 'BW' and vari2[1][:2] in ('N(', 'LI', 'SP') and
																	vari4[1][:4] != 'WW(v' and vari5[1][:4] != 'WW(v'):
																count += 1
															elif (vari1[1][:2] == 'BW' and vari2[1][:2] == 'VN' and
																	(vari3[1][:1] == 'N' or vari4[1][:1] == 'N') and
																	vari4[1][:4] not in ('WW(v', 'WW(i', 'ADJ(') and
																	vari5[1][:4] not in ('WW(v', 'WW(i', 'ADJ(')):
																count += 1
														elif vari1[1][:2] == 'LI':
															if (vari_min1[1][:5] not in ('WW(vd', 'ADJ(p', 'ADJ(v') and
																	vari3[1][:5] not in ('WW(vd', 'ADJ(p', 'ADJ(v') and
																	vari4[1][:5] not in ('WW(vd', 'ADJ(p', 'ADJ(v') and
																	vari5[1][:5] not in ('WW(vd', 'ADJ(p', 'ADJ(v') and
																	vari6[1][:5] not in ('WW(vd', 'ADJ(p', 'ADJ(v')):
																if not (vari4[1][:2] == 'VZ' or vari5[1][:2] == 'VZ' or
																		vari6[1][:2] == 'VZ'):
																	count += 1
																elif vari4[0] == 'van':
																	count += 1
														elif (vari1[1][:2] in ('SP', 'VN') and vari2[1][:2] == 'LI'):
															if (vari4[1][:5] not in ('WW(vd', 'ADJ(p', 'ADJ(v') and
																	vari5[1][:5] not in ('WW(vd', 'ADJ(p', 'ADJ(v')):
																count += 1
														elif vari2[1] == 'LET()':
															if vari1[1][:1] in ('N', 'S'):
																count += 1
										else:
											if (vari_min1[1][:2] != 'WW' and vari_min1[1][:2] != 'VZ'):
												if (vari_min1[1][:2] in ('N(', 'AD') and  # Adjective is nominative.
														not re.search(r'VZ (LI )?(AD )?', tag_prev)):
													count += 1
											else:
												if re.search(aux, vari_min1[2]):
													if (vari_min2[1][:1] == 'N' or vari_min2[1][:5] == 'ADJ(n'):
														count += 1
													else:
														if (vari_min2[1][:2] == 'VZ' and vari_min3[1][:2] in ('N(', 'SP')):
															count += 1
												else:
													if (vari_min1[1][:2] == 'VZ' and vari_min2[1][:2] in ('N(', 'SP')):
														count += 1

						# Modal verbs.
                        # Always count lexical verb.
                        # Never count all other instances.
						elif re.search(modal, vari[2]):
							if not (re.search(r'WW', tag_next) or re.search(r'WW', tag_prev)):
								# Lexical verb is missing, modal verb = replacement proposition.
								count += 1
							elif not (vari[2][:4] == '[zal' or vari1[1][:2] == 'WW' or vari_min1[1][:2] == 'WW'):
								if re.search(r'\[ga', vari[2]):
									if vari_min1[0] == 'te':
										if vari_min2[1][:4] != 'WW(i':
											count += 1
									elif not ((vari2[1][:4] == 'WW(i' and vari1[1][:2] not in ('LE', 'VG')) or
											  (vari3[1][:4] == 'WW(i' and (vari1[1][:2] not in ('LE', 'VG') and
																		   vari2[:2] not in ('LE', 'VG'))) or
											  (vari4[1][:4] == 'WW(i' and (vari1[1][:2] not in ('LE', 'VG') and
																		   vari2[1][:2] not in ('LE', 'VG') and
																		   vari3[1][:2] not in ('LE', 'VG'))) or
											  (vari5[1][:4] == 'WW(i' and (vari1[1][:2] not in ('LE', 'VG') and
																		   vari2[1][:2] not in ('LE', 'VG') and
																		   vari3[1][:2] not in ('LE', 'VG') and
																		   vari4[1][:2] not in ('LE', 'VG'))) or
											  (vari6[1][:4] == 'WW(i' and (vari1[1][:2] not in ('LE', 'VG') and
																		   vari2[1][:2] not in ('LE', 'VG') and
																		   vari3[1][:2] not in ('LE', 'VG') and
																		   vari4[1][:2] not in ('LE', 'VG'))) or
											  (vari7[1][:4] == 'WW(i' and (vari1[1][:2] not in ('LE', 'VG') and
																		   vari2[1][:2] not in ('LE', 'VG') and
																		   vari3[1][:2] not in ('LE', 'VG') and
																		   vari4[1][:2] not in ('LE', 'VG')))):
										count += 1
								elif not re.search(mod1, tag_without):
									if vari2[1][:4] != 'WW(i':
										if vari_min1[1] == 'LET()':
											if not (re.search(mod2, tag_without) or vari1[1][:2] == 'LE'):
												# Matches long distance infinitives:
												if not (((vari3[1][:4] == 'WW(i' or vari4[1][:4] == 'WW(i') and
														 (vari2[1] != 'LET()' and vari3[1] != 'LET()')) or
														((vari5[1][:4] == 'WW(i' or vari6[1][:4] == 'WW(i') and
														 (vari2[1] != 'LET()' and vari3[1] != 'LET()' and
														  vari4[1] != 'LET()' and vari5[1]) != 'LET()')):
													count += 1
										elif vari1[1] == 'LET()':
											if vari_min1[1][:2] == 'VN':
												count += 1
										elif (vari1[1][:2] == 'VG' and vari1[0] == 'dat'):
											count += 1

						# Secondary copula.
						# Always count sec. copula, accompanied by Noun phrase.
						# Always count lexical verbs.
						# Never count all other instances.
						elif re.search(sec_cop, vari[2]):
							if re.search(r'blijf', vari[2]):
								# Never count auxiliary verbs:
								if not ((vari1[1][:4] in ('WW(i', 'WW(v') or vari_min1[1].startswith('WW(i')) or
										(vari2[1][:4] in ('WW(i', 'WW(v') and vari1[1][:2] not in ('LE', 'VG')) or
										(vari3[1][:4] in ('WW(i', 'WW(v') and (vari1[1][:2] not in ('LE', 'VG') and
																			   vari2[:2] not in ('LE', 'VG'))) or
										(vari4[1][:4] in ('WW(i', 'WW(v') and (vari1[1][:2] not in ('LE', 'VG') and
																			   vari2[1][:2] not in ('LE', 'VG') and
																			   vari3[1][:2] not in ('LE', 'VG'))) or
										(vari5[1][:4] in ('WW(i', 'WW(v') and (vari1[1][:2] not in ('LE', 'VG') and
																			   vari2[1][:2] not in ('LE', 'VG') and
																			   vari3[1][:2] not in ('LE', 'VG') and
																			   vari4[1][:2] not in ('LE', 'VG'))) or
										(vari6[1][:4] in ('WW(i', 'WW(v') and (vari1[1][:2] not in ('LE', 'VG') and
																			   vari2[1][:2] not in ('LE', 'VG') and
																			   vari3[1][:2] not in ('LE', 'VG') and
																			   vari4[1][:2] not in ('LE', 'VG'))) or
										(vari7[1][:4] in ('WW(i', 'WW(v') and (vari1[1][:2] not in ('LE', 'VG') and
																			   vari2[1][:2] not in ('LE', 'VG') and
																			   vari3[1][:2] not in ('LE', 'VG') and
																			   vari4[1][:2] not in ('LE', 'VG')))):
									if vari_min1[0] in ('hier', 'daar', 'waar'):
										# Always count lexical verb (~zich bevinden).
										count += 1
									elif not (re.search(r'ADJ\([vp]', vari1[1]) and vari2[1][:4] != 'VZ(i'):
										if not (vari_min1[1][:5] in ('ADJ(v', 'ADJ(p', 'WW(vd') and
												not vari_min2[1][:2] in ('LI')):
											if vari1[0] in ('bij', 'in', 'hier'):
												# Always count lexical verb (~zich bevinden).
												count += 1
											elif vari_min1[1][:3] == 'ADJ':
												# Adjective functions as noun, verb is counted.
												count += 1
											else:
												if (vari_min1[0] == 'te' or re.search(modal, vari_min1[2])):
													if not vari_min2[1][:3] in ('WW(', 'ADJ'):
														count += 1
												elif re.search(r' (bij|in) (\w+ )+[Bb]l(ij|ee?)[fv](en)?t? ', sent_without):
													count += 1
												elif not re.search(r'[Bb]l(ij|ee?)[fv](en)?t? (\w+ )*(\w+n) \W', sent_without):
													if (vari1[1][:2] == 'LI' and vari3[1][:5] not in ('ADJ(v', 'ADJ(p')):
														count += 1
													elif re.search(r'[Bb]l(ij|ee?)[fv](en)?t? (\w+ )*(over|achter|af|uit|op) ', sent_without):
														count += 1
													elif (vari3[1].startswith('N') and vari4[1][:5] not in ('ADJ(v', 'ADJ(p')):
														count += 1
													else:
														if not (vari1[1] == 'BW' and vari2[1][:5] in ('ADJ(v', 'ADJ(p')):
															count += 1

							elif re.search(r'\[dunk\]', vari[2]):
								count = count  # Never count auxiliary verb 'dunken'.

							elif re.search(r'kom', vari[2]):
								# Matches any form of 'voorkomen'.
								if vari[0].startswith('voorkomend'):
									# Should be tagged as adjective.
									count += 1
								elif not (vari_min1[1][:7] == 'VNW(bez' or vari_min1[1][:2] == 'LI'):
									# Should be tagged as noun.
									if (vari_min1[0] == 'te' or re.search(modal, vari_min1[2])):
										count += 1  # Always count lexical verb.
							else:
								if (re.search(op, sent_without) and re.search(r'lijk', vari[2])):
									# Always count lexical verb 'lijken op'.
									count += 1
								elif (re.search(licht, sent_without) and re.search(r'schijn', vari[2])):
									# Always count lexical verb '[licht] schijnen'.
									count += 1
								elif (re.search(r'blijk', vari[2]) and
										(re.search(r' zag', sent_without) or re.search(bleek, sent_without))):
									# Frequently falsely tagged adjective 'bleek'.
									count += 1
								elif not re.search(kop_hulp, sent_next):
									if not re.search(alsof_dat, sent_without):
										if not re.search(kop_het, sent_without):
											if not (re.search(r'[Nn]aar ((he)|(\'))t schijnt', sent_without) and
													vari[0] == 'schijnt'):
												if vari1[1][:2] != 'VZ':
													if (vari_min1[1][:5] not in ('ADJ(v', 'ADJ(p', 'WW(vd')):
														if vari1[1][:5] in ('ADJ(v', 'ADJ(p'):
															if (vari2[1][:1] == 'N' or vari3[1][:1] == 'N'):
																count += 1
														elif vari2[1][:5] in ('ADJ(v', 'ADJ(p', 'WW(vd'):
															if vari1[1].startswith('LI'):
																count += 1
														elif (re.search(r'[ov]d,[np]', vari1[1][:7]) or
																re.search(r'[ov]d,[np]', vari2[1][:7]) or
																re.search(r'[ov]d,[np]', vari3[1][:7])):
															count += 1
														elif vari1[1].startswith('SP'):
															count += 1
														elif vari2[1].startswith('N') or vari2[1].startswith('SP'):
															count += 1
														elif vari3[1].startswith('N') or vari3[1].startswith('SP'):
															if not vari4[1].startswith('WW'):
																count += 1
														elif vari4[1].startswith('N'):
															count += 1

					
					# Lexical verbs.
					# Never count verbs that function as nouns.
					else:
						if re.search(r'WW.*\,nom\,', vari[1]):
							if vari_min1[0] in ("'t", 'het') and vari_min2[0] == 'aan':
								count += 1  # Falsely tagged lexical verbs.
						elif re.search(r'(^\[((begin)|(lig)|(sta)|(zit))\])', vari[2]):
							if not re.search(r'(^(\w+ )*te \w+n)', sent_next):
								# Never count replacement auxiliary verbs.
								count += 1
							elif re.search(r' ((om)|(dat)|(en)) (\w+ )*te \w+n', sent_next):
								if not re.search(r' te (\w+ )*te', sent_next):
									count += 1
						else:
							count += 1
		
		# Sentence PID
		sentence_pid = count/wordcount
		result_dict['per_sentence'].append(sentence_pid)
		
		# Add the proposition count of each sentence to the total proposition count.
		total_propcount += count
		total_wordcount += wordcount
		total_baseline += baseline_count
		baseline_count = 0
		wordcount = 0
		count = 0
	
	# Measure propositional idea density
	# by dividing the total proposition count by the total number of words.
	prop_density = total_propcount / total_wordcount
	result_dict['overall'] = prop_density
	
	# Measure the baseline score
	# by dividing the total baseline count by the total number of words.
	baseline_score = total_baseline / total_wordcount

	if output == 'PID':
		return result_dict # prop_density
	elif output == 'BL':
		return baseline_score

with open('participant_lines_image_mapping.json') as f:
    mapping = json.load(f)

scores = dict()
for filename in glob.glob('./Parsed/*.txt'):
    output = Dutch_idea_density(filename, output='PID')
    participant = re.findall('(\d+).txt', filename)[0]
    scores[participant] = {'overall': output['overall'],
                           'per_sentence': dict(zip(mapping[participant], output['per_sentence']))}
    
    with open('PID.json','w') as f:
        json.dump(scores, f, indent=2)
