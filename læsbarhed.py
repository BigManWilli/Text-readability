import re

class TextAnalysis:
    def __init__(self, text):
        self.text = text
        self.sentences = self.split_into_sentences()
        self.words = self.split_into_words()
        self.long_words = [word for word in self.words if len(word) > 6]
        self.word_count = len(self.words)
        self.char_count = len(self.text)
        self.sentence_count = len(self.sentences)
        self.gammeldags_sprog_detected = False  # Ny variabel til at spore gammeldags sprog

    def split_into_sentences(self):
        # Justeret regex for at ignorere ellipsen (...) og kun splitte på punktum, spørgsmålstegn og udråbstegn
        return [s.strip() for s in re.split(r'(?<!\.\.\.)[.!?]', self.text) if s.strip()]

    def split_into_words(self):
        # Brug regular expressions til at finde ord i teksten
        return re.findall(r'\b\w+\b', self.text)

    # --- Syntaktisk Analyse med ny rangliste ---
    def syntactic_analysis(self):
        # Opdel sætninger i korte og lange
        short_sentences = [s for s in self.sentences if len(s.split()) <= 10]
        long_sentences = [s for s in self.sentences if len(s.split()) > 10]  # Lang sætning defineret som > 10 ord

        # Beregn kompleksitetsfaktorer
        sentence_length_factor = self.word_count / self.sentence_count  # Gennemsnitligt antal ord pr. sætning
        
        # Skaler vægten af lange sætninger (f.eks. reducere vægten fra tidligere)
        long_sentence_factor = len(long_sentences) * 1  # Lavere vægt på lange sætninger

        # Beregn den samlede kompleksitetsfaktor
        complexity_score = sentence_length_factor + (long_sentence_factor*100)/self.word_count

        # Ny rangliste (1-10)
        if complexity_score < 15:
            rank = 1
        elif complexity_score < 20:
            rank = 2
        elif complexity_score < 25:
            rank = 3
        elif complexity_score < 30:
            rank = 4
        elif complexity_score < 35:
            rank = 5
        elif complexity_score < 40:
            rank = 6
        elif complexity_score < 45:
            rank = 7
        elif complexity_score < 50:
            rank = 8
        elif complexity_score < 55:
            rank = 9
        else:
            rank = 10

        return {
            "short_sentences": len(short_sentences),
            "long_sentences": len(long_sentences),
            "average_sentence_length": sentence_length_factor,
            "complexity_score": round(complexity_score, 1),
            "rank": rank
        }

    # --- Sproglig Analyse ---
    def linguistic_analysis(self):
        categories = {
            'ordsprog_talemåder': self.find_proverbs(),
            'symbolik': self.find_symbolism(),
            'metaforer': self.find_metaphors(),
            'gammeldags_sprog': self.check_for_gammeldags_sprog()  # Tjek for gammeldags sprog
        }
        return categories

    def find_proverbs(self):
        # Ord og talemåder, der kan indikere ordsprog
        proverbs = ['slå to fluer med ét smæk', 'oppe i skyerne', 'at gå som katten om den varme grød']
        return [phrase for phrase in self.sentences if any(proverb in phrase for proverb in proverbs)]

    def find_symbolism(self):
        # Eksempler på symbolik
        symbols = ['blomst', 'mørke', 'lys', 'hav', 'sol', 'sky']
        return [word for word in self.words if word.lower() in symbols]

    def find_metaphors(self):
        # Metaforer: Simpel tilgang til at finde sætninger, der indeholder metaforer
        metaphor_patterns = ['som en', 'er som']
        return [sentence for sentence in self.sentences if any(phrase in sentence for phrase in metaphor_patterns)]

    # --- Tjek for gammeldags sprog ---
    def check_for_gammeldags_sprog(self):
        gammeldags_keywords = ['aa', 'ae']  # Søger efter gammeldags sprog
        gammeldags_found = [word for word in self.words if any(keyword in word for keyword in gammeldags_keywords)]

        if gammeldags_found and not self.gammeldags_sprog_detected:
            self.gammeldags_sprog_detected = True  # Hvis gammeldags sprog er fundet, så markér det som opdaget
            return ["Gammeldags sprog er fundet i teksten: " + ", ".join(gammeldags_found)]
        else:
            return []

    # --- Beregn kompleksitet baseret på alle faktorer ---
    def total_complexity(self):
        syntax_score = self.syntactic_analysis()["complexity_score"]
        
        # Beregn tekstlængdekompleksitet (jo længere, desto højere score)
        length_score = self.char_count / 500  # Jo længere teksten er, jo højere kompleksitet

        # Sproglig analyse
        linguistic_score = sum([len(val) for val in self.linguistic_analysis().values()])  # Hvis mange stilistiske elementer, højere score

        # Hvis gammeldags sprog blev fundet, øg sværhedsgraden en gang
        if self.gammeldags_sprog_detected:
            length_score += 10  # Øg sværhedsgraden en smule

        # Total kompleksitet
        total_complexity_score = syntax_score + length_score + linguistic_score

        # Rangliste: Afgør kompleksiteten på en skala fra 1 til 10
        if total_complexity_score < 10:
            rank = 1
        elif total_complexity_score < 15:
            rank = 2
        elif total_complexity_score < 20:
            rank = 3
        elif total_complexity_score < 25:
            rank = 4
        elif total_complexity_score < 30:
            rank = 5
        elif total_complexity_score < 35:
            rank = 6
        elif total_complexity_score < 40:
            rank = 7
        elif total_complexity_score < 45:
            rank = 8
        elif total_complexity_score < 50:
            rank = 9
        else:
            rank = 10

        return {
            "Total Complexity Score": round(total_complexity_score, 1),
            "Rank": rank,
        }

    # --- Ranglistebeskrivelse ---
    def rank_description(self, rank):
        if rank == 1:
            return "Meget let tekst for alle læsere, børnelitteratur."
        elif rank == 2:
            return "Let tekst for øvede læsere, ugebladslitteratur."
        elif rank == 3:
            return "Let tekst for erfarne læsere, simpel skønlitteratur."
        elif rank == 4:
            return "Middel, dagblade og tidsskrifter."
        elif rank == 5:
            return "Middel, let faglitteratur og populærvidenskabelige bøger."
        elif rank == 6:
            return "Svær, akademisk niveau, videnskabelige artikler."
        elif rank == 7:
            return "Svær, teknisk faglitteratur, specialistbøger."
        elif rank == 8:
            return "Meget svær, kompleks akademisk eller teknisk tekst."
        elif rank == 9:
            return "Ekstremt svær, teknisk, lovtekster og akademiske udgivelser."
        else:
            return "Ekstremt svær, meget kompleks faglitteratur på højeste niveau."

# Eksempel på brug
if __name__ == "__main__":
    text = input("Indsæt en tekst til analyse: ")

    analysis = TextAnalysis(text)
    
    # Syntaktisk analyse
    syntactic_result = analysis.syntactic_analysis()
    print("\nSyntaktisk Analyse:", syntactic_result)
    
    # Sproglig analyse
    linguistic_result = analysis.linguistic_analysis()
    print("\nSproglig Analyse:", linguistic_result)
    
    # Total kompleksitet
    total_complexity_result = analysis.total_complexity()
    print(f"\nTotal Komplekstitet: {total_complexity_result['Total Complexity Score']} - Rank: {total_complexity_result['Rank']}")
    
    # Rangliste beskrivelse
    rank = total_complexity_result["Rank"]
    description = analysis.rank_description(rank)
    print(f"\nRangliste (1-10): {rank} - {description}")