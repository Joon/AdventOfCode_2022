
var inputLines = File.ReadAllLines("day11_input.txt");
var monkeys = Parser.ParseLines(inputLines);

var commonDenominator = new List<long>(monkeys.Values.Select(m => m.Divisor)).Aggregate((x, y) => x * y);
Console.WriteLine($"Common Denominator: {commonDenominator}");

for (int i = 0; i < 10000; i++)
{
    Console.WriteLine($"Round {i}");
    foreach (var monkey in monkeys.Values)
    {
        foreach(var item in monkey.ItemsHeld)
        {
            monkey.InspectionCount++;
            var newVal = monkey.Operation(item.WorryLevel);
            item.WorryLevel = newVal % commonDenominator;
            if(monkey.Test(item.WorryLevel))
            {
                monkeys[monkey.TrueDestinationMonkey].ItemsHeld.Add(item);
            } else
            {
                monkeys[monkey.FalseDestinationMonkey].ItemsHeld.Add(item);
            }
        }
        monkey.ItemsHeld.Clear();
    }
}

var inspectionCounts = new List<long>(monkeys.Values.Select(v => v.InspectionCount));
inspectionCounts.Sort();
inspectionCounts.Reverse();
Console.WriteLine($"Monkey Business is {inspectionCounts[0] * inspectionCounts[1]}");


class Item
{
    public long WorryLevel { get; set; }
}

class Monkey
{   
    public Monkey()
    {
        InspectionCount = 0;
    }

    private List<Item> _itemsInspected = new List<Item>();

    public int MonkeyIdentifier { get; set; }
    public long InspectionCount { get; set; }

    public Func<long, long>? Operation { get; set; }

    public long Divisor { get; set; }
    public Func<long, bool>? Test { get; set; }

    public int TrueDestinationMonkey { get; set; }
    public int FalseDestinationMonkey { get; set; }

    public List<Item> ItemsHeld { get { return _itemsInspected; } }
}

static class Parser
{
    public static Dictionary<int, Monkey> ParseLines(string[] inputLines)
    {
        var monks = new Dictionary<int, Monkey>();
        Monkey currentMonk = null;
        foreach (string line in inputLines)
        {
            if (line.StartsWith("Monkey"))
            {
                if (currentMonk != null)
                    monks[currentMonk.MonkeyIdentifier] = currentMonk;
                currentMonk = new Monkey();
                currentMonk.MonkeyIdentifier = Convert.ToInt32(line.Split(' ')[1].Replace(":", ""));
            }
            if (line.Trim().StartsWith("Starting items:"))
            {
                var itemIds = line.Split(": ")[1];
                foreach (var itemId in itemIds.Split(", "))
                {
                    Item item = new Item();
                    item.WorryLevel = Convert.ToInt32(itemId);
                    currentMonk.ItemsHeld.Add(item);
                }
            }
            if (line.Trim().StartsWith("Operation"))
            {
                var operationTokens = line.Split(": ")[1].Split(" ");
                var monkOperator = operationTokens[3];
                if (operationTokens[4] == "old")
                {
                    if (monkOperator == "*")
                    {
                        currentMonk.Operation = (x) => x * x;
                    }
                    else if (monkOperator == "+")
                    {
                        currentMonk.Operation = (x) => x + x;
                    }
                    else
                    {
                        throw new InvalidOperationException("Unknown Monkey operator");
                    }
                }
                else { 
                    var monkValue = Convert.ToInt64(operationTokens[4]);
                    if (monkOperator == "*")
                    {
                        currentMonk.Operation = (x) => x * monkValue;
                    }
                    else if (monkOperator == "+")
                    {
                        currentMonk.Operation = (x) => x + monkValue;
                    }
                    else
                    {
                        throw new InvalidOperationException("Unknown Monkey operator");
                    }
                }
            }
            if (line.Trim().StartsWith("Test"))
            {
                var operationTokens = line.Split(": ")[1].Split(" ");
                var monkOperator = operationTokens[0];
                var monkValue = Convert.ToInt64(operationTokens[2]);
                currentMonk.Divisor = monkValue;
                if (monkOperator == "divisible")
                {
                    currentMonk.Test = (x) => x % monkValue == 0;
                }
                else
                {
                    throw new InvalidOperationException("Unknown Monkey operator");
                }
            }
            if (line.Trim().StartsWith("If true:"))
            {
                var trueTokens = line.Split(": ")[1].Split(" ");
                currentMonk.TrueDestinationMonkey = Convert.ToInt32(trueTokens[3]);
            }
            if (line.Trim().StartsWith("If false:"))
            {
                var trueTokens = line.Split(": ")[1].Split(" ");
                currentMonk.FalseDestinationMonkey = Convert.ToInt32(trueTokens[3]);
            }                        
        }
        monks[currentMonk.MonkeyIdentifier] = currentMonk;
        return monks;
    }
}