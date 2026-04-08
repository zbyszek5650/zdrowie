import streamlit as st
import pandas as pd

st.set_page_config(page_title="Cyberatak na Szpital - Symulacja", layout="wide", page_icon="🏥")

# --- STAN GRY ---
@st.cache_resource
def get_game_state():
    return {
        "round": 0, 
        "teams": {}, 
        "active_scenario": "Wariant A: Ransomware i paraliż systemu HIS" 
    }

state = get_game_state()

# --- BAZA SCENARIUSZY MEDYCZNYCH ---
ALL_SCENARIOS = {
    "Wariant A: Ransomware i paraliż systemu HIS": {
        1: {
            "title": "Runda 1: Pierwsze symptomy infekcji",
            "desc": "Godzina 14:00. Lekarze na Szpitalnym Oddziale Ratunkowym (SOR) zgłaszają, że system HIS (Hospital Information System) działa bardzo wolno. Na kilku komputerach w rejestracji pojawiły się dziwne, czarne ekrany. Pacjenci w kolejce zaczynają się denerwować.",
            "questions": {
                "IT": {
                    "label": "Decyzja IT / Cyberbezpieczeństwo:",
                    "options": {
                        "Natychmiastowe odcięcie SOR od głównej sieci szpitalnej (Downtime prewencyjny)": {"pat": 0, "avl": -20, "fin": -5, "comp": +10},
                        "Analiza logów w tle i próba zdalnego restartu stacji w rejestracji": {"pat": -10, "avl": +5, "fin": 0, "comp": -10},
                    }
                },
                "Med": {
                    "label": "Decyzja Medyczna / Koordynator Oddziału:",
                    "options": {
                        "Wdrożenie procedury 'Downtime': przejście na papierową dokumentację i ręczne zlecenia badań": {"pat": +15, "avl": 0, "fin": -5, "comp": +10},
                        "Wstrzymanie wypisów i przyjęć planowych do czasu powrotu systemu": {"pat": -15, "avl": 0, "fin": -15, "comp": -5},
                    }
                },
                "Dir": {
                    "label": "Decyzja Dyrekcji Szpitala:",
                    "options": {
                        "Powiadomienie Centrum e-Zdrowia (CeZ) o potencjalnych problemach technicznych": {"pat": 0, "avl": 0, "fin": 0, "comp": +15},
                        "Brak eskalacji na zewnątrz, czekamy na diagnozę wewnętrzną IT": {"pat": 0, "avl": 0, "fin": 0, "comp": -15},
                    }
                }
            }
        },
        2: {
            "title": "Runda 2: Żądanie Okupu i Stan Wyjątkowy",
            "desc": "Godzina 16:30. Diagnoza jest najgorsza z możliwych: Ransomware zaszyfrował bazy danych pacjentów (wyniki badań, historie chorób, grupy krwi). Na ekranach wyświetla się żądanie 50 Bitcoinów. Laboratorium nie może przesyłać wyników, a lekarze nie znają dawek leków dla pacjentów na oddziałach.",
            "questions": {
                "IT": {
                    "label": "Decyzja IT / Cyberbezpieczeństwo:",
                    "options": {
                        "Twardy reset i wyłączenie głównych serwerów, wezwanie CERT Polska": {"pat": -10, "avl": -30, "fin": -10, "comp": +25},
                        "Próba odzyskania danych z porannych kopii zapasowych bez wyłączania sieci (Ryzyko infekcji backupu)": {"pat": -25, "avl": -10, "fin": -20, "comp": -20},
                    }
                },
                "Med": {
                    "label": "Decyzja Medyczna / PR:",
                    "options": {
                        "Przekierowanie karetek do innych szpitali, wypisywanie pacjentów stabilnych": {"pat": +20, "avl": 0, "fin": -20, "comp": +10},
                        "Próba kontynuacji leczenia wszystkich pacjentów 'na ślepo' (bazując na wywiadzie od pacjenta)": {"pat": -40, "avl": 0, "fin": 0, "comp": -30},
                    }
                },
                "Dir": {
                    "label": "Decyzja Dyrekcji Szpitala:",
                    "options": {
                        "Kategoryczna odmowa negocjacji z hakerami, powołanie sztabu kryzysowego z Policją": {"pat": 0, "avl": 0, "fin": +10, "comp": +20},
                        "Nawiązanie tajnego kontaktu z hakerami, próba negocjacji okupu za klucz deszyfrujący": {"pat": -10, "avl": 0, "fin": -40, "comp": -25},
                    }
                }
            }
        },
        3: {
            "title": "Runda 3: Rekonwalescencja i Audyt",
            "desc": "Dzień 3. Trwa mozolne odtwarzanie systemów. Szpital działa w trybie ostro-dyżurowym. Pod placówką stoją wozy transmisyjne stacji telewizyjnych, a do drzwi puka kontrola z Urzędu Ochrony Danych Osobowych (UODO) pytając o wyciek danych wrażliwych (medycznych).",
            "questions": {
                "IT": {
                    "label": "Decyzja IT / Architektura:",
                    "options": {
                        "Odbudowa sieci od zera z pełną mikrosegmentacją (proces potrwa tygodnie)": {"pat": +10, "avl": -15, "fin": -20, "comp": +20},
                        "Szybkie załatanie dziur i przywrócenie starej architektury, by wznowić przyjęcia": {"pat": -20, "avl": +20, "fin": +10, "comp": -25},
                    }
                },
                "Med": {
                    "label": "Decyzja PR / Komunikacja:",
                    "options": {
                        "Otwarty komunikat o naruszeniu danych, uruchomienie infolinii dla pacjentów": {"pat": +10, "avl": 0, "fin": -10, "comp": +25},
                        "Zasłanianie się tajemnicą śledztwa, odmawianie komentarzy o wycieku": {"pat": -10, "avl": 0, "fin": -20, "comp": -20},
                    }
                },
                "Dir": {
                    "label": "Decyzja Dyrekcji Szpitala:",
                    "options": {
                        "Szkolenia antyphishingowe dla 100% personelu przed dopuszczeniem do nowych systemów": {"pat": +15, "avl": -5, "fin": -10, "comp": +15},
                        "Ignorowanie szkoleń, zrzucenie winy za atak wyłącznie na wadliwy program antywirusowy": {"pat": -15, "avl": 0, "fin": 0, "comp": -20},
                    }
                }
            }
        }
    },
    
    "Wariant B: Atak na urządzenia medyczne (IoT) i OiTM": {
        1: {
            "title": "Runda 1: Utrata synchronizacji aparatury",
            "desc": "Godzina 03:00 w nocy. Oddział Intensywnej Terapii Medycznej (OiTM). Kardiomonitory nagle tracą łączność z centralą na biurku pielęgniarek. Dwie pompy infuzyjne (podłączone do Wi-Fi) zaczynają emitować fałszywe alarmy krytyczne. Panika na oddziale.",
            "questions": {
                "IT": {
                    "label": "Decyzja IT / SOC:",
                    "options": {
                        "Natychmiastowe odcięcie sieci Wi-Fi dla urządzeń medycznych (IoT) w całym skrzydle": {"pat": +10, "avl": -20, "fin": -5, "comp": +5},
                        "Zdalny restart centrali monitorującej (utrzymanie sieci w działaniu)": {"pat": -15, "avl": +10, "fin": 0, "comp": -10},
                    }
                },
                "Med": {
                    "label": "Decyzja Medyczna / Pielęgniarki:",
                    "options": {
                        "Przejście na manualne, fizyczne monitorowanie pacjentów (wymaga 100% obłożenia personelu)": {"pat": +25, "avl": 0, "fin": -10, "comp": +10},
                        "Zignorowanie anomalii jako 'kolejnej awarii sprzętu', wyciszenie alarmów": {"pat": -40, "avl": 0, "fin": 0, "comp": -30},
                    }
                },
                "Dir": {
                    "label": "Decyzja Dyrekcji Szpitala:",
                    "options": {
                        "Skierowanie dodatkowego personelu medycznego z innych oddziałów na OiTM": {"pat": +20, "avl": 0, "fin": -15, "comp": 0},
                        "Czekanie na raport z porannej zmiany": {"pat": -20, "avl": 0, "fin": 0, "comp": -10},
                    }
                }
            }
        },
        2: {
            "title": "Runda 2: Szantaż na życiu pacjentów",
            "desc": "Godzina 05:00. Na drukarkach w dyżurkach drukuje się manifest hakerski. Przestępcy udowadniają, że mają dostęp do interfejsów pomp infuzyjnych i grożą zdalną zmianą dawek leków ratujących życie, jeśli szpital nie zapłaci w ciągu 2 godzin.",
            "questions": {
                "IT": {
                    "label": "Decyzja IT / Cyberbezpieczeństwo:",
                    "options": {
                        "Fizyczne wyciągnięcie kabli zasilających routery na OiTM (tzw. air-gap)": {"pat": +20, "avl": -30, "fin": -5, "comp": +15},
                        "Próba znalezienia złośliwego oprogramowania w sieci i jego kwarantanna online": {"pat": -30, "avl": -5, "fin": 0, "comp": -20},
                    }
                },
                "Med": {
                    "label": "Decyzja Medyczna / Koordynator:",
                    "options": {
                        "Odłączenie chorych od inteligentnych pomp i podawanie leków metodami grawitacyjnymi / strzykawkowymi": {"pat": +25, "avl": -10, "fin": -5, "comp": +10},
                        "Ewakuacja całego oddziału OiTM do innego szpitala na sygnale": {"pat": -15, "avl": -20, "fin": -30, "comp": +5},
                    }
                },
                "Dir": {
                    "label": "Decyzja Dyrekcji Szpitala (Ustawa o KSC):",
                    "options": {
                        "Zgłoszenie incydentu krytycznego do CSIRT GOV i Policji w trybie pilnym": {"pat": 0, "avl": 0, "fin": 0, "comp": +30},
                        "Zatajenie charakteru ataku. Próba samodzielnej negocjacji okupu dla ratowania pacjentów": {"pat": -10, "avl": 0, "fin": -30, "comp": -40},
                    }
                }
            }
        },
        3: {
            "title": "Runda 3: Dochodzenie po incydencie",
            "desc": "Dzień następny. Sieć zabezpieczona fizycznie. Okazało się, że luki pochodziły z niezaktualizowanego oprogramowania (firmware) pomp zakupionych 8 lat temu. NFZ grozi wstrzymaniem finansowania oddziału z powodu niespełnienia norm bezpieczeństwa.",
            "questions": {
                "IT": {
                    "label": "Decyzja IT / Infrastruktura:",
                    "options": {
                        "Wydzielenie osobnej, hermetycznej sieci VLAN wyłącznie dla urządzeń ratujących życie (IoMT)": {"pat": +15, "avl": +10, "fin": -15, "comp": +20},
                        "Podłączenie sprzętu z powrotem do ogólnej sieci po zmianie haseł na trudniejsze": {"pat": -25, "avl": +20, "fin": +5, "comp": -30},
                    }
                },
                "Med": {
                    "label": "Decyzja PR / Komunikacja:",
                    "options": {
                        "Zawieszenie przyjmowania ostrego dyżuru i szczera komunikacja o audycie sprzętu": {"pat": +10, "avl": -15, "fin": -15, "comp": +10},
                        "Komunikowanie 'chwilowych usterek technicznych', kontynuacja przyjęć do innych sal": {"pat": -15, "avl": +10, "fin": +10, "comp": -20},
                    }
                },
                "Dir": {
                    "label": "Decyzja Dyrekcji Szpitala:",
                    "options": {
                        "Rozpoczęcie programu wymiany przestarzałego sprzętu medycznego (potężne koszty)": {"pat": +25, "avl": +10, "fin": -40, "comp": +20},
                        "Pozwanie producenta pomp o wypuszczenie wadliwego oprogramowania w celu uniknięcia kosztów": {"pat": -5, "avl": 0, "fin": +15, "comp": 0},
                    }
                }
            }
        }
    }
}

# --- FUNKCJE POMOCNICZE ---
def calculate_score(team_name):
    # Punkty startowe (100 punktów w każdej kategorii)
    pat, avl, fin, comp = 100, 100, 100, 100
    active_scenario_data = ALL_SCENARIOS[state["active_scenario"]]
    
    for r in range(1, state["round"] + 1):
        if r in state["teams"][team_name]["decisions"]:
            for role, choice in state["teams"][team_name]["decisions"][r].items():
                impact = active_scenario_data[r]["questions"][role]["options"][choice]
                pat += impact["pat"]
                avl += impact["avl"]
                fin += impact["fin"]
                comp += impact["comp"]
    return max(0, min(150, pat)), max(0, min(150, avl)), max(0, min(150, fin)), max(0, min(150, comp))

def render_progress_bar(label, value, is_critical=False):
    if is_critical:
        color = "green" if value > 80 else "orange" if value > 50 else "red"
    else:
        color = "green" if value > 70 else "orange" if value > 40 else "red"
        
    st.markdown(f"**{label}: {value}/100**")
    st.markdown(
        f"""<div style="width: 100%; background-color: #e0e0e0; border-radius: 5px; margin-bottom: 10px;">
        <div style="width: {min(value, 100)}%; background-color: {color}; height: 24px; border-radius: 5px;"></div>
        </div>""", unsafe_allow_html=True
    )

# --- WIDOKI ---
def login_view():
    st.title("🏥 Cyberatak na Szpital - Symulacja Sztabu Kryzysowego")
    st.write("W grze chronisz pacjentów, ciągłość leczenia oraz zmagasz się z wymogami KSC/RODO.")
    
    with st.expander("📱 Opcje dla Prowadzącego: Wyświetl kod QR dla personelu/studentów"):
        game_url = st.text_input("Wklej tutaj link do aplikacji:")
        if game_url:
            qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=250x250&data={game_url}"
            st.image(qr_url, caption="Zeskanuj telefonem, aby dołączyć")

    st.divider()
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Wejście dla Zespołów")
        team_name = st.text_input("Podaj nazwę Placówki (np. Szpital Wojewódzki):")
        if st.button("Dołącz do Sztabu"):
            if team_name:
                if team_name not in state["teams"]:
                    state["teams"][team_name] = {"decisions": {}, "ready": False}
                st.session_state["role"] = "team"
                st.session_state["team_name"] = team_name
                st.rerun()
            else:
                st.error("Wymagana nazwa szpitala!")
                
    with col2:
        st.subheader("Panel Koordynatora (Wykładowcy)")
        admin_pass = st.text_input("Hasło (domyślnie: admin):", type="password")
        if st.button("Zaloguj jako Koordynator"):
            if admin_pass == "admin":
                st.session_state["role"] = "admin"
                st.rerun()
            else:
                st.error("Odmowa dostępu!")

def admin_view():
    st.title("👨‍⚕️ Panel Sterowania Symulacją")
    
    if state["round"] == 0:
        st.warning("Szpital funkcjonuje normalnie. Wybierz scenariusz ataku przed startem dyżuru.")
        selected = st.selectbox("Wybierz rodzaj incydentu:", list(ALL_SCENARIOS.keys()), index=list(ALL_SCENARIOS.keys()).index(state["active_scenario"]))
        if selected != state["active_scenario"]:
            state["active_scenario"] = selected
            st.success(f"Zmieniono scenariusz na: {selected}")
    else:
        st.info(f"Trwa kryzys: **{state['active_scenario']}**")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Bieżąca Runda", state["round"] if state["round"] < 4 else "Raport Podyżurowy")
        if state["round"] < 4:
            if st.button("Uruchom następną rundę ⏩", type="primary"):
                state["round"] += 1
                for t in state["teams"]: state["teams"][t]["ready"] = False
                st.rerun()
        else:
            if st.button("Zakończ dyżur i Resetuj 🔄"):
                state["round"] = 0
                state["teams"] = {}
                st.rerun()
                
    with col2:
        st.write("### Status Oddziałów (Zespołów)")
        if not state["teams"]:
            st.info("Oczekujemy na gotowość personelu...")
        for t, data in state["teams"].items():
            status = "✅ Decyzje podjęte" if data["ready"] else "⏳ Narada sztabu..."
            st.write(f"- **{t}**: {status}")

    st.divider()
    st.write("### Tablica Monitorowania (KPI na żywo)")
    if state["teams"]:
        scores = []
        for t in state["teams"]:
            p, a, f, c = calculate_score(t)
            scores.append({"Placówka": t, "Zabezpieczenie Pacjentów": p, "Dostępność IT": a, "Finanse/PR": f, "Zgodność z Prawem": c})
        st.dataframe(pd.DataFrame(scores).style.background_gradient(cmap='RdYlGn', subset=['Zabezpieczenie Pacjentów', 'Zgodność z Prawem']), use_container_width=True)

def team_view():
    team = st.session_state["team_name"]
    st.title(f"🚨 Sztab Kryzysowy: {team}")
    
    with st.sidebar:
        st.header("Stan Szpitala")
        p, a, f, c = calculate_score(team)
        render_progress_bar("❤️ Życie i Zdrowie Pacjentów", p, is_critical=True)
        render_progress_bar("🖥️ Dostępność Systemów", a)
        render_progress_bar("💰 Finanse i Wizerunek", f)
        render_progress_bar("⚖️ Compliance (MZ, RODO, KSC)", c)
        st.warning("Pamiętajcie: Utrata systemów to problem, ale spadek zdrowia pacjentów poniżej 50 punktów to prokuratorskie zarzuty dla Dyrekcji!")

    if state["round"] == 0:
        st.info("Trwa spokojny dyżur. Ustalcie w zespole, kto podejmuje decyzje z ramienia Dyrekcji, Kadr Medycznych i Działu IT. Oczekujcie na sygnał od Koordynatora.")
        if st.button("Odśwież status"): st.rerun()
        
    elif 1 <= state["round"] <= 3:
        r = state["round"]
        active_scenario_data = ALL_SCENARIOS[state["active_scenario"]]
        scenario = active_scenario_data[r]
        
        st.header(scenario["title"])
        st.error(f"**Raport incydentu:** {scenario['desc']}")
        
        if state["teams"][team]["ready"]:
            st.success("Procedury awaryjne wdrożone. Czekajcie na rozwój sytuacji (następna runda).")
            if st.button("Odśwież ekran"): st.rerun()
        else:
            st.write("---")
            st.write("### Wymagane pilne decyzje Sztabu:")
            
            with st.form(f"form_r{r}"):
                choices = {}
                for role, q_data in scenario["questions"].items():
                    st.subheader(q_data["label"])
                    choices[role] = st.radio(f"Wybór {role}", list(q_data["options"].keys()), label_visibility="collapsed")
                    st.write("")
                
                if st.form_submit_button("Wydaj Polecenia (Zatwierdź) 📝"):
                    if r not in state["teams"][team]["decisions"]:
                        state["teams"][team]["decisions"][r] = {}
                    state["teams"][team]["decisions"][r] = choices
                    state["teams"][team]["ready"] = True
                    st.rerun()

    elif state["round"] == 4:
        st.header("🏁 Zakończenie Kryzysu - Raport Pokontrolny")
        p, a, f, c = calculate_score(team)
        
        st.subheader("Ocena placówki:")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Bezpieczeństwo Pacjentów", p)
        col2.metric("Dostępność", a)
        col3.metric("Finanse/PR", f)
        col4.metric("Zgodność", c)
        
        st.write("---")
        if p < 50:
            st.error("Wyrok Prokuratora: **ZAGROŻENIE ŻYCIA PACJENTÓW.** Paraliż informatyczny doprowadził do tragicznych błędów medycznych. Dyrekcja i szef IT usłyszą zarzuty karne z art. 160 kk. Zignorowaliście najważniejszy priorytet w medycynie.")
        elif c < 40:
            st.error("Wyrok Regulatora: **KATASTROFA PRAWNA.** Ukrywanie faktu cyberataku doprowadziło do zaangażowania UODO i Ministerstwa Zdrowia. Gigantyczne kary finansowe pogrążą szpital i doprowadzą do zwolnienia personelu zarządczego.")
        elif p > 70 and c > 50:
            st.success("Wyrok: **PRAWIDŁOWE ZARZĄDZANIE KRYZYSEM.** Straciliście pieniądze i systemy, sprzęt musi zostać wymieniony, ale zachowaliście trzeźwy umysł. Ochroniliście pacjentów przed śmiercią, a organizację przed zarzutami karnymi poprzez transparentną współpracę ze służbami państwowymi.")
        else:
            st.info("Wyrok: **PRZETRWANIE SZPITALA.** Sytuacja uległa stabilizacji, pacjenci są bezpieczni, jednak straty finansowe i spadek zaufania publicznego będą ciągnąć się za placówką przez lata.")

# --- ROUTING ---
if "role" not in st.session_state:
    login_view()
elif st.session_state["role"] == "admin":
    admin_view()
elif st.session_state["role"] == "team":
    team_view()