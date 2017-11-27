# Define compiler/linker:
CXX    = g++
LINK = g++
YACC  = bison-2.4
#YACC  = bison
LEX   = flex

# Define compiler/linker flags:
DEBUG = -g
OPTIMIZE = -O2

CXXFLAGS = $(DEBUG) $(OPTIMIZE) -I.
LDFLAGS = $(DEBUG) $(OPTIMIZE) -L.

LEX_SRC=ppddl.lex
LEX_OBJ=lex.yy.cc


YACC_SRC=ppddl.yy
YACC_OBJ=ppddl.tab.cc ppddl.tab.hh location.hh position.hh stack.hh

SOURCES=BuchiAutomaton.cc base.cc basic.cc char_map.cc lex.yy.cc name.cc ppddl.tab.cc  parser.cc ltpddl2pddl.cc problem.cc ptr_table.cc string_table.cc

OBJECTS=$(SOURCES:.cc=.o)

TARGET=ltpddl2pddl

%.o : %.c %.cc

$(LEX_OBJ) : $(LEX_SRC) $(YACC_OBJ)
	$(LEX) -o $(LEX_OBJ) $(LEX_SRC)
#	$(LEX) --header-file=$(LEX_OBJ:.cc=.h) -o $(LEX_OBJ) $(LEX_SRC)
	
$(YACC_OBJ) : $(YACC_SRC)
	$(YACC) $(YACC_SRC)
	
libp.a: ../ltl2ba-1.1/*.o $(OBJECTS)
	ar cr libp.a $(OBJECTS) ../ltl2ba-1.1/*.o
	ranlib libp.a	
	
.PHONY : clean
clean:
	rm -f $(YACC_OBJ) $(LEX_OBJ) *.o $(TARGET)

$(TARGET) : libp.a
	$(LINK) $(LDFLAGS) -lp -o $(TARGET)


all: $(TARGET)

	