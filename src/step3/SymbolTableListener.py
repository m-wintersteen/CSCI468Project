from antlr4 import *
from LittleListener import LittleListener
from LittleParser import LittleParser

class SymbolTableListener(LittleListener):

    # initialize symbol table datastructure here
    def enterProgram(self, ctx:LittleParser.ProgramContext):
        self.error = None
        self.symbolTable = {}
        self.previousScopes = []
        self.block = 0
        self.recordVars = False
        self.enterScope('GLOBAL')

    # print symbol table entries here
    def exitProgram(self, ctx:LittleParser.ProgramContext):
        if self.error:
            print(f'DECLARATION ERROR {self.error}')
        else:
            for scope, table in self.symbolTable.items():
                print(f'Symbol table {scope}')
                for var, attr in table.items():
                    if (attr['value']):
                        print(f'name {var} type {attr["type"]} value {attr["value"]}')
                    else:
                        print(f'name {var} type {attr["type"]}')
                print()


    # Enter a parse tree produced by LittleParser#string_decl.
    def enterString_decl(self, ctx:LittleParser.String_declContext):
        # print("string declaration")
        var = ctx.getChild(1).getText()
        val = ctx.getChild(3).getText()
        self.addSymbol(var, 'STRING', val)

    # Exit a parse tree produced by LittleParser#string_decl.
    def exitString_decl(self, ctx:LittleParser.String_declContext):
        pass

    # Enter a parse tree produced by LittleParser#var_decl.
    def enterVar_decl(self, ctx:LittleParser.Var_declContext):
        self.vars = []
        self.recordVars = True;


    # Exit a parse tree produced by LittleParser#var_decl.
    def exitVar_decl(self, ctx:LittleParser.Var_declContext):
        varType = ctx.getChild(0).getText()
        for var in self.vars:
            self.addSymbol(var, varType)
        self.recordVars = False

    # Enter a parse tree produced by LittleParser#id.
    def enterId(self, ctx:LittleParser.IdContext):
        if (self.recordVars):
            self.vars.append(ctx.getText())

    # HANDLE SCOPES HERE

    # Enter a parse tree produced by LittleParser#func_decl.
    def enterFunc_decl(self, ctx:LittleParser.Func_declContext):
        functionName = ctx.getChild(2).getText()
        self.enterScope(functionName)

    # Exit a parse tree produced by LittleParser#func_decl.
    def exitFunc_decl(self, ctx:LittleParser.Func_declContext):
        self.exitScope()

    # Enter a parse tree produced by LittleParser#param_decl.
    def enterParam_decl(self, ctx:LittleParser.Param_declContext):
        varType = ctx.getChild(0).getText()
        var = ctx.getChild(1).getText()
        self.addSymbol(var, varType)

    # Exit a parse tree produced by LittleParser#param_decl.
    def exitParam_decl(self, ctx:LittleParser.Param_declContext):
        pass

    # Enter a parse tree produced by LittleParser#if_stmt.
    def enterIf_stmt(self, ctx:LittleParser.If_stmtContext):
        self.enterBlock()

    # Exit a parse tree produced by LittleParser#if_stmt.
    def exitIf_stmt(self, ctx:LittleParser.If_stmtContext):
        self.exitBlock()

    # Enter a parse tree produced by LittleParser#else_part.
    def enterElse_part(self, ctx:LittleParser.Else_partContext):
        if (ctx.children != None):
            self.enterBlock()

    # Exit a parse tree produced by LittleParser#else_part.
    def exitElse_part(self, ctx:LittleParser.Else_partContext):
        if (ctx.children != None):
            self.exitBlock()

    # Enter a parse tree produced by LittleParser#while_stmt.
    def enterWhile_stmt(self, ctx:LittleParser.While_stmtContext):
        self.enterBlock()

    # Exit a parse tree produced by LittleParser#while_stmt.
    def exitWhile_stmt(self, ctx:LittleParser.While_stmtContext):
        self.exitBlock()


    # UTILITY FUNCTIONS FOR SCOPES AND SYMBOL TABLES

    def enterScope(self, scope):
        # print(f'entering scope {scope}')
        if hasattr(self, 'scope'):
            self.previousScopes.append(self.scope)
        self.scope = scope;
        self.symbolTable[self.scope] = {}

    def exitScope(self):
        # print(f'leaving scope {self.scope}')
        self.scope = self.previousScopes.pop()
        # print(f'entering scope {self.scope}')

    def enterBlock(self):
        self.block = self.block + 1
        self.enterScope(f'BLOCK {self.block}')
        pass

    def exitBlock(self):
        self.exitScope()
        pass

    def addSymbol(self, var, t, val=None):
        if not var in self.symbolTable[self.scope]:
            self.symbolTable[self.scope][var] = {'value':val,'type':t}
        else:
            if not self.error:
                self.error = var
        