module MiniUCI.Chess () where

import Data.Array

data PieceKind
  = Bishop
  | King
  | Knight
  | Pawn
  | Queen
  | Rook
  deriving (Eq)

data PieceColor
  = Black
  | White
  deriving (Eq)

pieceColorAsFen :: PieceColor -> String
pieceColorAsFen color = case color of
  Black -> "b"
  White -> "w"

data Piece = Piece PieceKind PieceColor deriving (Eq)

piecesAsFen :: Array Int (Maybe Piece) -> String
piecesAsFen pieces = _

data CastlingRights = CastlingRights
  { blackKingCanCastle :: Bool,
    blackQueenCanCastle :: Bool,
    whiteKingCanCastle :: Bool,
    whiteQueenCanCastle :: Bool
  }
  deriving (Eq)

data Board = Board
  { boardPieces :: Array Int (Maybe Piece),
    boardTurn :: PieceColor,
    boardCastling :: CastlingRights,
    boardEnPassantIndex :: Maybe Int,
    boardHalfmoveClock :: Int,
    boardFullmoveNumber :: Int
  }
  deriving (Eq)

boardAsFen :: Board -> String
boardAsFen board =
  concat
    [ piecesAsFen $ boardPieces board,
      pieceColorAsFen $ boardTurn board,
      castlingAsFen $ boardCastling board,
      enPassantAsFen $ boardEnPassantIndex board,
      show $ boardHalfmoveClock board,
      show $ boardFullmoveNumber board
    ]
