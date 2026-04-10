## Resources

- Solidity (Argot Project GitHub Repository)  
  https://github.com/argotorg/solidity  
  A resource related to Solidity and smart contract analysis.

  https://en.wikipedia.org/wiki/Solidity

- Solidity Practice
  https://www.tutorialspoint.com/solidity/solidity_overview.htm

- Mastering Ethereum: 2nd Edition
  https://masteringethereum.xyz/



\section{Blockchain vs. Ethereum}

Blockchain is a general technology, while Ethereum is one specific blockchain platform.

A blockchain can be understood as a distributed public ledger maintained by many computers. Instead of being stored and controlled by a single company or bank, the record is shared across many nodes, and each node helps verify and preserve the data.

An analogy is that \textbf{blockchain is like the category ``operating system,'' while Ethereum is like one specific operating system such as Windows or macOS}. In the same way, blockchain is a broad concept, and Ethereum is one concrete implementation of that idea.

Another analogy is that \textbf{blockchain is like the word ``vehicle,'' while Ethereum is like a specific car model}. The first word describes a whole class of systems, and the second refers to one member of that class.

For example, Bitcoin has its own blockchain, Ethereum has its own blockchain, and other systems such as Solana also have their own blockchains. They all belong to the larger category of blockchain systems, but they are not the same network.

The special importance of Ethereum is that it does not only record transactions. It also allows developers to deploy and execute programs, which are called smart contracts.

\section{Ethereum vs. Bitcoin}

Ethereum and Bitcoin are both blockchain-based systems, but they were designed with different goals in mind.

Bitcoin is mainly designed for storing and transferring value. Its core purpose is to function as a decentralized form of digital money. Many people therefore describe Bitcoin as \textbf{digital gold}.

Ethereum, by contrast, is designed not only for transferring value but also for running programmable applications on-chain. It provides an environment in which developers can write smart contracts and build decentralized applications.

A useful analogy is that \textbf{Bitcoin is like a calculator, while Ethereum is like a computer}. A calculator is powerful for a narrow task and is relatively simple. A computer can do much more, but it is also more complex and more likely to encounter software bugs.

For example, if Alice wants to send Bob 0.02 BTC, the Bitcoin system mainly checks whether Alice owns the coins, verifies the transaction, and updates the ledger. This is primarily a value-transfer task.

By contrast, suppose a university wants to build an automatic scholarship distribution system. The rules may say that money is locked in a program, only students satisfying certain GPA conditions may claim it, each student may claim only once, and the claim period closes after a deadline. This type of logic is much more naturally expressed on Ethereum through a smart contract.

Thus, Bitcoin focuses more on money and payments, whereas Ethereum focuses more on programmability and applications.

\section{Relationship Among Bitcoin, Blockchain, Ethereum, and Solidity}

These concepts are closely related, but they refer to different layers.

\begin{itemize}
    \item \textbf{Blockchain:} the general technology of a decentralized ledger.
    \item \textbf{Bitcoin:} a blockchain system mainly used for digital money and value transfer.
    \item \textbf{Ethereum:} a blockchain platform that supports smart contracts.
    \item \textbf{Smart Contract:} a program deployed on a blockchain that automatically enforces rules.
    \item \textbf{Solidity:} the programming language used to write smart contracts on Ethereum.
\end{itemize}

A simple way to connect them is the following:

\begin{quote}
Blockchain is the broad technology. Ethereum is a specific blockchain designed to run programs. Solidity is the language used to write those programs. Bitcoin is another blockchain system, but it is more focused on digital money than on general programmability.
\end{quote}

\section{A Running Example}

Consider the idea of an automatic savings box.

In a traditional system, a company might run a server that stores users' balances and decides when withdrawals are allowed. In a blockchain-based system, the rules can instead be written into a smart contract.

For example, the contract may state that two users deposit funds, the money remains locked until the end of the month, and no one may withdraw early. Once deployed on Ethereum, the contract automatically enforces these rules.

In this example:

\begin{itemize}
    \item the \textbf{blockchain} is the shared ledger and execution environment,
    \item \textbf{Ethereum} is the specific platform on which the program runs,
    \item the \textbf{smart contract} is the actual savings-box program,
    \item and \textbf{Solidity} is the language used to write that program.
\end{itemize}

This example also helps explain why correctness matters so much. If the withdrawal rule is implemented incorrectly, the error may lead to direct financial loss, and fixing the issue after deployment may be difficult or impossible.

\section{Why These Distinctions Matter for Research}

These distinctions are important because research in programming languages and formal methods is usually not about cryptocurrency prices themselves. Instead, the main concern is whether the programs that manage digital assets behave correctly.

Bitcoin is useful for understanding digital assets and decentralized value transfer. Ethereum is especially important because it supports programmable contracts. Solidity then becomes the direct object of study, since bugs in Solidity contracts can cause serious and irreversible consequences.

Therefore, from a research perspective, one natural progression is:

\begin{quote}
understand blockchain as the general setting, understand Ethereum as the programmable platform, and then study Solidity as the language in which smart contracts are written and verified.
\end{quote}
