using System;
using System.Security.Cryptography;

namespace blackjack
{
	public class Hand
	{
		public List<string> hand = new List<string>();

		private int wager = 0;
        private int score = 0;

        public int Wager
		{
			get {return wager;}
	        set {wager = value;}
		}

		public int Score
		{
			get {return score;}
	        set {score = value;}
		}

        ///Creates hand with two cards (used for initial user hand)
		public Hand(int bet)
		{
			hand.Add(takecard());
            hand.Add(takecard());
			score = calculatescore(this.hand);
            wager = bet;
		}

        ///Used for initial dealer hand and for splits
        public Hand(string card, int bet)
		{
			hand.Add(card);
			score = calculatescore(this.hand);
            wager = bet;
		}

        ///Used to make sure that score is re-calculated when card is added to the list
        public void AddCard()
        {
            hand.Add(takecard());
            score=calculatescore(this.hand);
        }

        ///Used to add new cards from deck to hand
		public static string takecard()
        {
            string[] cards = new string[] {"2","3","4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"};
            return cards[RandomNumberGenerator.GetInt32(cards.Length)];
        }

		///Used to calculate score based on player or dealer cards
        public static int calculatescore(List<string> a)
        {
            int[] scores = new int[a.Count];
            for (int i = 0; i < a.Count(); i++)
            {
                if (!int.TryParse(a[i], out int r))
                {
                    if (a[i] == "A")
                        scores[i] = 11;
                    else
                        scores[i] = 10;
                }
                else
                    scores[i] = r;
            }
            while (scores.Sum() > 21 && Array.IndexOf(scores,11)!=-1)
                scores[Array.IndexOf(scores,11)] = 1;

            return scores.Sum();
        }
	}
}
