:- dynamic sim/1,nao/1. 
:- dynamic animal/2.


start :- ['animals_data.pl'],
	(hypothesize(Animal)->
	write("O animal que voce esta pensando eh: "),write(Animal),nl,
	write("Acertei? (s/n)"),nl,
	read(X),nl,
	(
		X = 's' -> write('Sou um genio!'),undo;
		X = 'n' -> nl,learnAnimal(Animal),!
	);learnAnimal(unknown)).




check([]).

check([H|T]):-
  verify(H),check(T).

hypothesize(A) :- 
  animal(A,H),
  check(H).




ask(Characteristic) :-
	write(Characteristic), write("(s/n)"),nl,
	read(Answer),nl,
	(Answer = 's' -> assertz(sim(Characteristic)),true; Answer = 'n' -> assertz(nao(Characteristic)),fail).
	


verify(S) :- (sim(S) -> true ; (nao(S) -> fail ; ask(S))). 



isEmpty([]).

isUnknown(unknown).

findSim(L) :- findall(X,sim(X), L).

learnAnimal(A) :-
	write('Putz... entao nao sei. Qual animal voce esta pensando?'),nl,
	read(X),nl,

	(
		isUnknown(A)->write('Qual pergunta eu devo fazer para saber que eh '),write(X),write('?'),nl,
		read(Y),nl,
		findSim(P),
			(
			isEmpty(P)->asserta(animal(X,[Y]));
			append(P,[Y],J),
			assertz(animal(X,J))
			),
		write('Obrigado! Vou anotar aqui pra proxima!'),nl,undo,save;


		write('Qual pergunta eu devo fazer para diferenciar '),write(A),write(' de '),write(X),write('?'),nl,
		read(Y),nl,
		write('Obrigado! Vou anotar aqui pra proxima!'),nl,
		findSim(P),
		append(P,[Y],J),
		assertz(animal(X,J)),undo,save
	),undo.


save :-
    tell('animals_data.pl'),
    listing(animal),
    told.


undo :-
    retractall(sim(_)),retractall(nao(_)).
undo.
