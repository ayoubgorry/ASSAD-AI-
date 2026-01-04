import json
import os
from typing import List, Dict, Any
from langchain_core.documents import Document
from config import DATA_FOLDER, FILES, TEAM_ALIASES

# ============================================================================
# UTILITAIRES GÉNÉRAUX
# ============================================================================

def load_json_file(filename: str) -> List[Dict]:
    """Charge un fichier JSON avec gestion d'erreurs."""
    filepath = os.path.join(DATA_FOLDER, filename)
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"⚠️ Fichier non trouvé : {filepath}")
        return []
    except json.JSONDecodeError:
        print(f"⚠️ Erreur de décodage JSON : {filepath}")
        return []

def get_team_aliases(team_name: str) -> List[str]:
    """Retourne toutes les variantes d'un nom d'équipe."""
    for canonical, aliases in TEAM_ALIASES.items():
        if team_name in aliases:
            return aliases
    return [team_name]

def normalize_team_name(team_name: str) -> str:
    """Normalise le nom d'une équipe vers sa version canonique."""
    team_name_clean = team_name.strip()
    for canonical, aliases in TEAM_ALIASES.items():
        if team_name_clean in aliases:
            return canonical
    return team_name_clean

# ============================================================================
# FORMATTERS - MATCHS
# ============================================================================

def format_match_detailed(match: Dict) -> str:
    """Format détaillé d'un match avec toutes les informations."""
    equipe_dom = match.get("equipe_domicile", "N/A")
    equipe_ext = match.get("equipe_exterieur", "N/A")
    score = match.get("score", "-")
    
    text = f"═══════════════════════════════════════════════════════════\n"
    text += f"⚽ MATCH CAN 2025 - {match.get('match_n', 'N/A')}\n"
    text += f"═══════════════════════════════════════════════════════════\n\n"
    
    text += f"📅 Date: {match.get('date', 'N/A')}\n"
    text += f"🏆 Phase: {match.get('phase', 'N/A')} - {match.get('etape', '')}\n"
    text += f"🏟️ Stade: {match.get('stade', 'N/A')}\n"
    text += f"👥 Affluence: {match.get('affluence', 'N/A')} spectateurs\n"
    text += f"⚖️ Arbitre: {match.get('arbitre', 'N/A')}\n\n"
    
    text += f"📊 RÉSULTAT FINAL\n"
    text += f"{equipe_dom} {score} {equipe_ext}\n\n"
    
    # Buts
    text += f"⚽ BUTS MARQUÉS\n"
    buts_dom = match.get("buteurs_domicile", [])
    buts_ext = match.get("buteurs_exterieur", [])
    
    if buts_dom or buts_ext:
        for but in buts_dom:
            passe = f" (passe: {but.get('passe_decisive')})" if but.get('passe_decisive') else ""
            type_but = f" [{but.get('type')}]" if but.get('type') != 'normal' else ""
            text += f"  ⚽ {but.get('minute')}' - {but.get('joueur')} ({equipe_dom}){passe}{type_but}\n"
        
        for but in buts_ext:
            passe = f" (passe: {but.get('passe_decisive')})" if but.get('passe_decisive') else ""
            type_but = f" [{but.get('type')}]" if but.get('type') != 'normal' else ""
            text += f"  ⚽ {but.get('minute')}' - {but.get('joueur')} ({equipe_ext}){passe}{type_but}\n"
    else:
        text += "  Aucun but marqué (0-0)\n"
    
    # Cartons
    text += f"\n🟨 DISCIPLINE\n"
    cartons_dom = match.get("cartons_domicile", [])
    cartons_ext = match.get("cartons_exterieur", [])
    
    if cartons_dom or cartons_ext:
        for carton in cartons_dom:
            emoji = "🟥" if carton.get('type') == 'rouge' else "🟨"
            text += f"  {emoji} {carton.get('minute')}' - {carton.get('joueur')} ({equipe_dom})\n"
        
        for carton in cartons_ext:
            emoji = "🟥" if carton.get('type') == 'rouge' else "🟨"
            text += f"  {emoji} {carton.get('minute')}' - {carton.get('joueur')} ({equipe_ext})\n"
    else:
        text += "  Aucun carton distribué\n"
    
    text += f"\n═══════════════════════════════════════════════════════════"
    return text

def format_match_summary(match: Dict) -> str:
    """Format résumé court d'un match."""
    equipe_dom = match.get("equipe_domicile", "N/A")
    equipe_ext = match.get("equipe_exterieur", "N/A")
    score = match.get("score", "-")
    date = match.get("date", "N/A")
    
    text = f"Match CAN 2025 - {match.get('match_n')}: "
    text += f"{equipe_dom} {score} {equipe_ext} "
    text += f"({date}, {match.get('stade', 'N/A')})"
    
    buts = []
    for but in match.get("buteurs_domicile", []):
        buts.append(f"{but['joueur']} {but['minute']}'")
    for but in match.get("buteurs_exterieur", []):
        buts.append(f"{but['joueur']} {but['minute']}'")
    
    if buts:
        text += f" | Buteurs: {', '.join(buts)}"
    
    return text

# ============================================================================
# FORMATTERS - ÉQUIPES
# ============================================================================

def format_team_complete(team_name: str, data_sources: Dict) -> str:
    """Format complet d'une équipe avec toutes les données croisées."""
    
    # Recherche des données de l'équipe
    team_info = next((t for t in data_sources['teams'] 
                      if normalize_team_name(t.get('Equipe', '')) == normalize_team_name(team_name)), {})
    
    coach_info = next((c for c in data_sources['coaches'] 
                       if normalize_team_name(c.get('pays', '')) == normalize_team_name(team_name)), {})
    
    squad_info = next((s for s in data_sources['squads'] 
                       if normalize_team_name(s.get('team', '')) == normalize_team_name(team_name)), {})
    
    # Construction du texte
    text = f"═══════════════════════════════════════════════════════════\n"
    text += f"🏆 {team_name.upper()} - CAN 2025\n"
    text += f"═══════════════════════════════════════════════════════════\n\n"
    
    # Informations générales
    text += f"📋 INFORMATIONS GÉNÉRALES\n"
    aliases = get_team_aliases(team_name)
    text += f"Noms: {', '.join(aliases[:3])}\n"
    text += f"Participation: {team_info.get('Participation', 'N/A')}\n"
    text += f"Première participation: {team_info.get('Premiere_participation', 'N/A')}\n"
    text += f"Dernière participation: {team_info.get('Derniere_participation', 'N/A')}\n"
    text += f"Qualification: {team_info.get('Methode_qualification', 'N/A')}\n"
    text += f"Date de qualification: {team_info.get('Date_qualification', 'N/A')}\n\n"
    
    # Palmarès
    text += f"🏆 PALMARÈS\n"
    text += f"Meilleur résultat: {team_info.get('Meilleur_resultat', 'N/A')}\n"
    apparitions = team_info.get('Apparitions_precedentes', 'N/A')
    if len(apparitions) > 200:
        apparitions = apparitions[:200] + "..."
    text += f"Participations précédentes: {apparitions}\n\n"
    
    # Sélectionneur
    if coach_info:
        text += f"👔 SÉLECTIONNEUR\n"
        text += f"Nom: {coach_info.get('selectionneur', 'N/A')}\n"
        text += f"Catégorie: {coach_info.get('categorie', 'N/A')}\n"
        details = coach_info.get('details', '')
        if details:
            # Limiter la longueur des détails
            if len(details) > 300:
                details = details[:300] + "..."
            text += f"Détails: {details}\n"
        text += "\n"
    
    # Effectif
    if squad_info:
        squad = squad_info.get('squad', {})
        
        # Statistiques de l'effectif
        nb_gardiens = len(squad.get('goalkeepers', []))
        nb_defenseurs = len(squad.get('defenders', []))
        nb_milieux = len(squad.get('midfielders', []))
        nb_attaquants = len(squad.get('forwards', []))
        total = nb_gardiens + nb_defenseurs + nb_milieux + nb_attaquants
        
        text += f"👥 EFFECTIF COMPLET ({total} joueurs)\n\n"
        
        # Gardiens
        text += f"═══ GARDIENS ({nb_gardiens}) ═══\n"
        for i, player in enumerate(squad.get('goalkeepers', []), 1):
            text += f"{i}. {player.get('name', 'N/A')} - {player.get('club', 'N/A')}\n"
        
        # Défenseurs
        text += f"\n═══ DÉFENSEURS ({nb_defenseurs}) ═══\n"
        for i, player in enumerate(squad.get('defenders', []), 1):
            text += f"{i}. {player.get('name', 'N/A')} - {player.get('club', 'N/A')}\n"
        
        # Milieux
        text += f"\n═══ MILIEUX ({nb_milieux}) ═══\n"
        for i, player in enumerate(squad.get('midfielders', []), 1):
            text += f"{i}. {player.get('name', 'N/A')} - {player.get('club', 'N/A')}\n"
        
        # Attaquants
        text += f"\n═══ ATTAQUANTS ({nb_attaquants}) ═══\n"
        for i, player in enumerate(squad.get('forwards', []), 1):
            text += f"{i}. {player.get('name', 'N/A')} - {player.get('club', 'N/A')}\n"
        
        text += "\n"
    
    text += f"═══════════════════════════════════════════════════════════"
    return text

def format_team_summary(team_name: str, data_sources: Dict) -> str:
    """Format résumé court d'une équipe."""
    team_info = next((t for t in data_sources['teams'] 
                      if normalize_team_name(t.get('Equipe', '')) == normalize_team_name(team_name)), {})
    
    coach_info = next((c for c in data_sources['coaches'] 
                       if normalize_team_name(c.get('pays', '')) == normalize_team_name(team_name)), {})
    
    text = f"{team_name} - {team_info.get('Participation', 'N/A')} participation(s). "
    text += f"Meilleur résultat: {team_info.get('Meilleur_resultat', 'N/A')}. "
    
    if coach_info:
        text += f"Sélectionneur: {coach_info.get('selectionneur', 'N/A')}."
    
    return text

# ============================================================================
# FORMATTERS - JOUEURS
# ============================================================================

def format_player_card(player: Dict, team_name: str, position: str) -> str:
    """Format d'une fiche joueur individuelle."""
    text = f"👤 FICHE JOUEUR - CAN 2025\n\n"
    text += f"Nom: {player.get('name', 'N/A')}\n"
    text += f"Équipe: {team_name}\n"
    text += f"Poste: {position}\n"
    text += f"Club: {player.get('club', 'N/A')}\n"
    
    return text

# ============================================================================
# FORMATTERS - CLASSEMENTS
# ============================================================================

def format_group_standings(group_data: Dict) -> str:
    """Format du classement d'un groupe."""
    text = f"═══════════════════════════════════════════════════════════\n"
    text += f"📊 CLASSEMENT CAN 2025 - {group_data.get('Nom_Groupe', 'N/A')}\n"
    text += f"═══════════════════════════════════════════════════════════\n\n"
    
    text += f"{'Rang':<6}{'Équipe':<20}{'Pts':<6}{'J':<4}{'G':<4}{'N':<4}{'P':<4}{'BP':<5}{'BC':<5}{'Diff'}\n"
    text += "-" * 75 + "\n"
    
    for team in group_data.get('Classement', []):
        text += f"{team.get('Rang', ''):<6}"
        text += f"{team.get('Equipe', 'N/A'):<20}"
        text += f"{team.get('Pts', '0'):<6}"
        text += f"{team.get('Matchs_joues', '0'):<4}"
        text += f"{team.get('Gagnes', '0'):<4}"
        text += f"{team.get('Nuls', '0'):<4}"
        text += f"{team.get('Perdus', '0'):<4}"
        text += f"{team.get('Buts_pour', '0'):<5}"
        text += f"{team.get('Buts_contre', '0'):<5}"
        text += f"{team.get('Diff', '0')}\n"
    
    text += f"\n═══════════════════════════════════════════════════════════"
    return text

# ============================================================================
# FORMATTERS - STADES
# ============================================================================

def format_stadium_info(stadium: Dict) -> str:
    """Format des informations d'un stade."""
    text = f"🏟️ STADE CAN 2025\n\n"
    text += f"Nom: {stadium.get('Stade', 'N/A')}\n"
    text += f"Ville: {stadium.get('Ville', 'N/A')}\n"
    text += f"Capacité: {stadium.get('Capacité', 'N/A')} spectateurs\n"
    
    return text

# ============================================================================
# PROCESSEURS PRINCIPAUX
# ============================================================================

def process_matches(data: List[Dict]) -> List[Document]:
    """Traite tous les matchs et crée des documents."""
    documents = []
    
    for match in data:
        if "equipe_domicile" not in match:
            continue
        
        # =========================
        # MATCH DÉTAILLÉ (inchangé)
        # =========================
        content_detailed = format_match_detailed(match)
        metadata_detailed = {
            "type": "match_detailed",
            "match_number": match.get("match_n", "N/A"),
            "phase": match.get("phase", "N/A"),
            "group": match.get("etape", "N/A"),
            "team_home": normalize_team_name(match.get("equipe_domicile", "")),
            "team_away": normalize_team_name(match.get("equipe_exterieur", "")),
            "teams": [
                normalize_team_name(match.get("equipe_domicile", "")),
                normalize_team_name(match.get("equipe_exterieur", ""))
            ],
            "date": match.get("date_iso", match.get("date", "N/A")),
            "stadium": match.get("stade", "N/A"),
            "score": match.get("score", "-"),
            "source": "matches.json"
        }
        documents.append(Document(page_content=content_detailed, metadata=metadata_detailed))
        
        # =========================
        # MATCH RÉSUMÉ (inchangé)
        # =========================
        content_summary = format_match_summary(match)
        metadata_summary = metadata_detailed.copy()
        metadata_summary["type"] = "match_summary"
        documents.append(Document(page_content=content_summary, metadata=metadata_summary))

        # =========================
        # DOCUMENT ÉVÉNEMENT (FINAL / DEMI / QUART)
        # =========================
        if match.get("etape", "").lower() in ["finale", "demi-finale", "quart de finale"]:
            event_text = f"""
🏆 {match.get("etape").upper()} - CAN 2025

📅 Date : {match.get("date")}
🏟️ Stade : {match.get("stade")}
⚽ Match : {match.get("equipe_domicile")} vs {match.get("equipe_exterieur")}
🆔 Match : {match.get("match_n")}
""".strip()

            documents.append(
                Document(
                    page_content=event_text,
                    metadata={
                        "type": "event",
                        "event": match.get("etape").lower().replace(" ", "_"),
                        "phase": match.get("etape"),
                        "date": match.get("date_iso", ""),
                        "teams": metadata_detailed["teams"],
                        "stadium": match.get("stade"),
                        "source": "matches.json"
                    }
                )
            )
    
    return documents


def process_teams(data_sources: Dict) -> List[Document]:
    """Traite toutes les équipes et crée des documents."""
    documents = []
    
    for team_data in data_sources['teams']:
        team_name = team_data.get('Equipe', '')
        if not team_name:
            continue
        
        normalized_name = normalize_team_name(team_name)
        
        # Document complet
        content_complete = format_team_complete(team_name, data_sources)
        metadata_complete = {
            "type": "team_complete",
            "team_name": normalized_name,
            "team_aliases": get_team_aliases(team_name),
            "participation": team_data.get('Participation', 'N/A'),
            "best_result": team_data.get('Meilleur_resultat', 'N/A'),
            "source": "multiple"
        }
        documents.append(Document(page_content=content_complete, metadata=metadata_complete))
        
        # Document résumé
        content_summary = format_team_summary(team_name, data_sources)
        metadata_summary = metadata_complete.copy()
        metadata_summary["type"] = "team_summary"
        documents.append(Document(page_content=content_summary, metadata=metadata_summary))
    
    return documents

def process_players(data: List[Dict]) -> List[Document]:
    """Traite tous les joueurs et crée des documents."""
    documents = []
    
    for squad_data in data:
        team_name = squad_data.get('team', '')
        if not team_name:
            continue
        
        normalized_team = normalize_team_name(team_name)
        squad = squad_data.get('squad', {})
        
        # Traiter chaque poste
        position_map = {
            'goalkeepers': 'Gardien',
            'defenders': 'Défenseur',
            'midfielders': 'Milieu',
            'forwards': 'Attaquant'
        }
        
        for position_key, position_label in position_map.items():
            for player in squad.get(position_key, []):
                content = format_player_card(player, team_name, position_label)
                
                metadata = {
                    "type": "player",
                    "player_name": player.get('name', 'N/A'),
                    "team": normalized_team,
                    "position": position_label,
                    "club": player.get('club', 'N/A'),
                    "source": "squads.json"
                }
                
                documents.append(Document(page_content=content, metadata=metadata))
    
    return documents

def process_standings(data: List[Dict]) -> List[Document]:
    """Traite les classements et crée des documents."""
    documents = []
    
    for group in data:
        content = format_group_standings(group)
        
        teams_in_group = [team.get('Equipe', '') for team in group.get('Classement', [])]
        
        metadata = {
            "type": "standings",
            "group": group.get('Nom_Groupe', 'N/A'),
            "teams": [normalize_team_name(t) for t in teams_in_group],
            "source": "classements.json"
        }
        
        documents.append(Document(page_content=content, metadata=metadata))
    
    return documents

def process_stadiums(data: List[Dict]) -> List[Document]:
    """Traite les stades et crée des documents."""
    documents = []
    
    for stadium in data:
        content = format_stadium_info(stadium)
        
        metadata = {
            "type": "stadium",
            "stadium_name": stadium.get('Stade', 'N/A'),
            "city": stadium.get('Ville', 'N/A'),
            "capacity": stadium.get('Capacité', 'N/A'),
            "source": "stades.json"
        }
        
        documents.append(Document(page_content=content, metadata=metadata))
    
    return documents

# ============================================================================
# FONCTION PRINCIPALE
# ============================================================================

def load_all_can2025_data() -> List[Document]:
    """
    Charge et traite TOUS les fichiers JSON de la CAN 2025.
    Retourne une liste de Documents LangChain prêts pour le RAG.
    """
    print("🔄 Chargement des données CAN 2025...")
    
    # Chargement de tous les fichiers
    data_sources = {
        'matches': load_json_file(FILES['matches']),
        'teams': load_json_file(FILES['teams']),
        'coaches': load_json_file(FILES['coaches']),
        'squads': load_json_file(FILES['squads']),
        'stadiums': load_json_file(FILES['stadiums']),
        'standings': load_json_file(FILES['standings']),
        'best_thirds': load_json_file(FILES['best_thirds'])
    }
    
    all_documents = []
    
    # Traitement des matchs
    print("  ⚽ Traitement des matchs...")
    match_docs = process_matches(data_sources['matches'])
    all_documents.extend(match_docs)
    print(f"    ✅ {len(match_docs)} documents de matchs créés")
    
    # Traitement des équipes
    print("  🏆 Traitement des équipes...")
    team_docs = process_teams(data_sources)
    all_documents.extend(team_docs)
    print(f"    ✅ {len(team_docs)} documents d'équipes créés")
    
    # Traitement des joueurs
    print("  👤 Traitement des joueurs...")
    player_docs = process_players(data_sources['squads'])
    all_documents.extend(player_docs)
    print(f"    ✅ {len(player_docs)} documents de joueurs créés")
    
    # Traitement des classements
    print("  📊 Traitement des classements...")
    standing_docs = process_standings(data_sources['standings'])
    all_documents.extend(standing_docs)
    print(f"    ✅ {len(standing_docs)} documents de classements créés")
    
    # Traitement des stades
    print("  🏟️ Traitement des stades...")
    stadium_docs = process_stadiums(data_sources['stadiums'])
    all_documents.extend(stadium_docs)
    print(f"    ✅ {len(stadium_docs)} documents de stades créés")
    
    print(f"\n✅ TOTAL: {len(all_documents)} documents créés avec succès!")
    
    return all_documents

# ============================================================================
# UTILITAIRES D'EXPORT
# ============================================================================

def export_documents_to_txt(documents: List[Document], output_file: str = "can2025_chunks.txt"):
    """Exporte tous les documents dans un fichier texte pour inspection."""
    with open(output_file, 'w', encoding='utf-8') as f:
        for i, doc in enumerate(documents, 1):
            f.write(f"\n{'='*80}\n")
            f.write(f"DOCUMENT {i}/{len(documents)}\n")
            f.write(f"Type: {doc.metadata.get('type', 'unknown')}\n")
            f.write(f"{'='*80}\n\n")
            f.write(doc.page_content)
            f.write(f"\n\nMÉTADONNÉES:\n{json.dumps(doc.metadata, indent=2, ensure_ascii=False)}\n")
    
    print(f"📄 Documents exportés vers: {output_file}")

def get_documents_by_type(documents: List[Document], doc_type: str) -> List[Document]:
    """Filtre les documents par type."""
    return [doc for doc in documents if doc.metadata.get('type') == doc_type]

def get_documents_by_team(documents: List[Document], team_name: str) -> List[Document]:
    """Récupère tous les documents liés à une équipe."""
    normalized = normalize_team_name(team_name)
    results = []
    
    for doc in documents:
        # Vérifier dans team_name
        if doc.metadata.get('team_name') == normalized:
            results.append(doc)
        # Vérifier dans teams (liste)
        elif normalized in doc.metadata.get('teams', []):
            results.append(doc)
        # Vérifier dans team (string)
        elif doc.metadata.get('team') == normalized:
            results.append(doc)
    
    return results
