using System;
using System.Security.Cryptography;
using System.Threading.Tasks.Dataflow;
using static blackjack.Actions;

namespace blackjack
{
    class Program
    {
        public static int bank = 0;
        public static int startbank = 0;

        static void Main(string[] args)
        {
            Console.WriteLine("Let's play a little game of Blackjack.");

            ///Get and validate budget from player, also assign that value to startbank to use in endgame().
            getbudget();  
            startbank = bank;
                            
            Console.WriteLine($"\nYour budget is {bank} dollars.");
            Console.WriteLine("To play a round of Blackjack, you have to bet at least 1 dollar.");
            Console.WriteLine("You can quit game at any point by adding Q to console when it asks for your bet.");

            /// Here we start the game
            while (bank>0)
            {
                /// List to be used to hold all user hands
                List<Hand> alluserhands = new List<Hand>();

                /// Gets and validates users bet
                int bet = getuserbet();

                /// This part get initial cards for player and dealer, calculates scores and shows both.
                Hand userhand = new Hand(bet);
                Hand dealerhand = new Hand(Hand.takecard(),bet);
                showcards(userhand,dealerhand);

                /// If player has blackjack, this round is over, dealer pays 1,5 times bet and goes to next while iteration
                if (blackjackwin(userhand))
                    continue;

                /// If no blackjack, we need further input from player
                while(true)
                {
                    /// Next line asks for player action, validates it and assigns to input
                    string input = getandvalidateinput();

                    /// If player wants to "STAY", we break loop and continue with dealer turns and results.
                    if (input == "S")
                    { 
                        alluserhands.Add(userhand);
                        break;    
                    }

                    /// If "HIT" then we add another card on the table, calculate scores and show latest situation
                    else if (input=="H")
                    {
                        userhand.AddCard();
                        showcards(userhand,dealerhand);

                        /// If userpoints goes over 21 then it's a bust - round is over for player.
                        if (userhand.Score>21)
                        { 
                            alluserhands.Add(userhand);
                            break;
                        }
                    }

                    /// If player wants to "DOUBLE" we double wager, add one card and break loop.
                    else if (input=="D")
                    {   
                        ///Validates if user has enough balance for this action
                        if (userhand.Wager*2>bank)
                        {
                            Console.WriteLine("Insufficient bank balance");
                            continue;
                        }
                        userhand.Wager *=2;
                        userhand.AddCard();
                        showcards(userhand,dealerhand);
                        alluserhands.Add(userhand);
                        break;    
                    }

                    /// if player wants to "SPLIT"
                    else if (input=="X")
                    {
                        ///Validates if user has enough balance for this action 
                        if (userhand.Wager*2>bank)
                        {
                            Console.WriteLine("Insufficient bank balance");
                            continue;
                        }
                        ///Validates if both cards are of the same value.
                        if (calculatescore(userhand.hand[0]) != calculatescore(userhand.hand[1]))
                        {
                            Console.WriteLine("You can only split your hand if your initial two-card hand includes two cards of the same value!");
                            continue;
                        }

                        /// Creating list of lists to use foreach after
                        List<Hand> multiplehands = new List<Hand>() {userhand};

                        Console.WriteLine($"You have split {string.Join(" ", userhand.hand)} hand.");
                        multiplehands.Add(new Hand(userhand.hand.ElementAt(1),userhand.Wager));
                        
                        multiplehands[1].AddCard();
                        multiplehands[0].hand.Remove(multiplehands[0].hand.ElementAt(1));
                        multiplehands[0].AddCard();
                        Console.WriteLine($"New hands = {string.Join(" ", multiplehands[0].hand)} and {string.Join(" ", multiplehands[1].hand)}");


                        Console.Clear();

                        for (int i = 0; i < multiplehands.Count; i++)
                        {
                            Console.WriteLine($"Your bet is {multiplehands.Sum(x => x.Wager)} in total, bank balance {bank}");
                            bool split = false;

                            while(true)
                            {
                                Console.WriteLine($"\nHand at play: {String.Join(" ", multiplehands[i].hand)}  ({multiplehands[i].Score})");
                                input = getandvalidateinput();

                                if (input == "S")
                                    break;

                                else if (input=="H")
                                {
                                    multiplehands[i].AddCard();
                                    showcards(multiplehands[i],dealerhand);

                                    /// If over 21 - bust, break.
                                    if (multiplehands[i].Score>21) 
                                        break;
                                }

                                /// If Double, double wager, add card, break.
                                else if (input=="D")
                                {   
                                    ///Validates if user has enough balance for this action
                                    if (multiplehands.Sum(x => x.Wager)+multiplehands[i].Wager>bank)
                                    {
                                        Console.WriteLine("Insufficient bank balance");
                                        continue;
                                    }
                                    multiplehands[i].Wager *=2;
                                    multiplehands[i].AddCard();
                                    showcards(multiplehands[i],dealerhand);
                                    break;
                                }

                                else if (input=="X")
                                {   
                                    ///Validates if user has enough balance for this action
                                    if (multiplehands.Sum(x => x.Wager)+multiplehands[i].Wager>bank)
                                    {
                                        Console.WriteLine("Insufficient bank balance");
                                        continue;
                                    }
                                    if (calculatescore(multiplehands[i].hand[0]) != calculatescore(multiplehands[i].hand[1]))
                                    {
                                        Console.WriteLine("You can only split your hand if your initial two-card hand includes two cards of the same value!");
                                        continue;
                                    }

                                    Console.WriteLine($"You have split {string.Join(" ", multiplehands[i].hand)} hand.");
                                    multiplehands.Insert(i+1,new Hand(multiplehands[i].hand.ElementAt(1),multiplehands[i].Wager));
                                    multiplehands[i+1].AddCard();

                                    multiplehands[i].hand.Remove(multiplehands[i].hand.ElementAt(1));
                                    multiplehands[i].AddCard();
                                    Console.WriteLine($"New hands = {string.Join(" ", multiplehands[i].hand)} and {string.Join(" ", multiplehands[i+1].hand)}");

                                    i--;
                                    split = true;
                                    break;
                                }

                            }
                            if (!split)
                                alluserhands.Add(multiplehands[i]);
                        }
                        break;
                    }
                }

                if (alluserhands.Count == 1 && userhand.Score>21)
                {
                    bank -= userhand.Wager;
                    Console.WriteLine($"You went bust! You lost {userhand.Wager}, current bank balance {bank}");
                    continue;
                }

                /// Dealers turn to pick up cards, dealer has to HIT on <17 and STAY on >=17.
                Console.WriteLine("\nDealers turn:");

                while (dealerhand.Score<=16)
                    dealerhand.AddCard();

                /// Start to evaluate player hand(s) against dealer hand
                foreach (Hand hand in alluserhands)
                { 
                    showcards(hand,dealerhand);

                    /// If player has more than 21, he has lost, take wager from bank, display results.
                    if (hand.Score>21)
                    {
                        bank -= hand.Wager;
                        Console.WriteLine($"You went bust with \"{String.Join(" ", hand.hand)}\" hand. You lost {hand.Wager}, current bank balance {bank}");
                        continue;
                    }

                    /// If dealer went bust, player has won, add wager to bank and display result.
                    if (dealerhand.Score>21)
                    {
                        bank += hand.Wager;
                        Console.WriteLine($"Dealer went bust! You have won {hand.Wager} with \"{String.Join(" ", hand.hand)}\" hand, current bank balance {bank}");
                        continue;
                    }

                    ///If both are still in the game compare results and change bank balance
                    getresults(hand, dealerhand.Score);

                    /// If player is out of money, go to endgame and show results.
                    if (bank <=0)
                        endgame();
                }
            }
        }
    }
}
