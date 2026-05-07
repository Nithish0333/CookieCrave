import React, { useState, useEffect } from 'react';
import { Container, Card, Button, Row, Col, Badge, Alert, Modal } from 'react-bootstrap';
import { Trophy, Gift, Copy, Lock, PieChart, Sparkles, Layout, ArrowLeft } from 'lucide-react';
import discountService from '../services/discountService';
import './DiscountGamesPage.css';

const DiscountGamesPage = () => {
  const [activeGame, setActiveGame] = useState(null);
  const [userDiscounts, setUserDiscounts] = useState([]);
  const [gameStatus, setGameStatus] = useState({});
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [modalMessage, setModalMessage] = useState('');
  const [modalDiscount, setModalDiscount] = useState(0);

  useEffect(() => {
    initData();
  }, []);

  const initData = async () => {
    setLoading(true);
    await Promise.all([fetchDiscounts(), fetchGameStatus()]);
    setLoading(false);
  };

  const fetchDiscounts = async () => {
    try {
      const response = await discountService.getMyDiscounts();
      setUserDiscounts(response.data);
    } catch (error) {
      console.error('Error fetching discounts:', error);
    }
  };

  const fetchGameStatus = async () => {
    try {
      const response = await discountService.getGameStatus();
      setGameStatus(response.data);
    } catch (error) {
      console.error('Error fetching game status:', error);
    }
  };

  const handleClaimDiscount = async (gameType, discount) => {
    try {
      await discountService.claimDiscount(gameType, discount);
      await Promise.all([fetchDiscounts(), fetchGameStatus()]);
    } catch (error) {
      console.error('Error claiming discount:', error);
    }
  };

  // Spin the Wheel Game
  const [wheelSpinning, setWheelSpinning] = useState(false);
  const wheelDiscounts = [5, 10, 15, 20, 25, 30, 50];

  const spinWheel = () => {
    if (wheelSpinning || (gameStatus.spin_wheel && !gameStatus.spin_wheel.can_play)) return;
    setWheelSpinning(true);
    
    setTimeout(async () => {
      const randomDiscount = wheelDiscounts[Math.floor(Math.random() * wheelDiscounts.length)];
      setModalDiscount(randomDiscount);
      setModalMessage(`🎉 Congratulations! You won ${randomDiscount}% discount!`);
      await handleClaimDiscount('spin_wheel', randomDiscount);
      setShowModal(true);
      setWheelSpinning(false);
    }, 3000);
  };

  // Scratch Card Game
  const [scratchCards, setScratchCards] = useState([]);
  const [scratchGameWon, setScratchGameWon] = useState(false);
  const [scratchCount, setScratchCount] = useState(0);

  useEffect(() => {
    initScratchGame();
  }, []);

  const initScratchGame = () => {
    const discounts = [10, 20, 30, 50];
    const pool = [];
    // Ensure at least 3 of one value as a potential win
    const winningValue = discounts[Math.floor(Math.random() * discounts.length)];
    for(let i=0; i<3; i++) pool.push(winningValue);
    // Fill the rest randomly
    while(pool.length < 9) {
      pool.push(discounts[Math.floor(Math.random() * discounts.length)]);
    }
    // Shuffle
    const shuffled = pool.sort(() => Math.random() - 0.5);
    
    setScratchCards(shuffled.map(d => ({ revealed: false, discount: d })));
    setScratchGameWon(false);
    setScratchCount(0);
  };

  const revealCard = async (index) => {
    if (scratchGameWon || scratchCards[index].revealed || (gameStatus.scratch_card && !gameStatus.scratch_card.can_play)) return;
    
    const newCards = [...scratchCards];
    newCards[index].revealed = true;
    setScratchCards(newCards);
    
    const newCount = scratchCount + 1;
    setScratchCount(newCount);

    // Check for 3 matches
    const revealedValues = newCards.filter(c => c.revealed).map(c => c.discount);
    const counts = {};
    let winningDiscount = 0;
    
    for (const val of revealedValues) {
      counts[val] = (counts[val] || 0) + 1;
      if (counts[val] === 3) {
        winningDiscount = val;
        break;
      }
    }

    if (winningDiscount > 0) {
      setScratchGameWon(true);
      setModalDiscount(winningDiscount);
      setModalMessage(`🎊 Match 3! You won a ${winningDiscount}% discount code!`);
      await handleClaimDiscount('scratch_card', winningDiscount);
      setShowModal(true);
    } else if (newCount === 9) {
      // No win after all revealed
      setModalDiscount(0);
      setModalMessage(`😅 Better luck next time! No matching 3 found.`);
      await handleClaimDiscount('scratch_card', 0); // Record the play even if no win
      setShowModal(true);
      setScratchGameWon(true);
    }
  };

  const resetScratchGame = () => {
    if (gameStatus.scratch_card && !gameStatus.scratch_card.can_play) return;
    initScratchGame();
  };

  // Memory Match Game
  const [memoryCards, setMemoryCards] = useState([]);
  const [memoryFlipped, setMemoryFlipped] = useState([]);
  const [memoryMatches, setMemoryMatches] = useState(0);

  useEffect(() => {
    initMemoryGame();
  }, []);

  const initMemoryGame = () => {
    const items = ['🍪', '🧁', '🍩', '🍫'];
    const cards = [...items, ...items]
      .sort(() => Math.random() - 0.5)
      .map((icon, i) => ({ id: i, icon, matched: false, flipped: false }));
    setMemoryCards(cards);
    setMemoryFlipped([]);
    setMemoryMatches(0);
  };

  const flipMemoryCard = async (index) => {
    if (memoryFlipped.length === 2 || memoryCards[index].flipped || memoryCards[index].matched || (gameStatus.memory_match && !gameStatus.memory_match.can_play)) return;

    const newCards = [...memoryCards];
    newCards[index].flipped = true;
    setMemoryCards(newCards);

    const newFlipped = [...memoryFlipped, index];
    setMemoryFlipped(newFlipped);

    if (newFlipped.length === 2) {
      if (memoryCards[newFlipped[0]].icon === memoryCards[newFlipped[1]].icon) {
        newCards[newFlipped[0]].matched = true;
        newCards[newFlipped[1]].matched = true;
        setMemoryCards(newCards);
        setMemoryMatches(prev => {
          const newMatchCount = prev + 1;
          if (newMatchCount === 4) {
            const discount = 40;
            setModalDiscount(discount);
            setModalMessage(`🧠 Memory Master! You won ${discount}% discount!`);
            handleClaimDiscount('memory_match', discount);
            setShowModal(true);
          }
          return newMatchCount;
        });
        setMemoryFlipped([]);
      } else {
        setTimeout(() => {
          const resetCards = [...newCards];
          resetCards[newFlipped[0]].flipped = false;
          resetCards[newFlipped[1]].flipped = false;
          setMemoryCards(resetCards);
          setMemoryFlipped([]);
        }, 1000);
      }
    }
  };

  const resetMemoryGame = () => {
    if (gameStatus.memory_match && !gameStatus.memory_match.can_play) return;
    initMemoryGame();
  };

  if (loading) return (
    <div className="d-flex justify-content-center align-items-center vh-100 bg-white">
      <div className="text-center">
        <div className="spinner-grow text-primary mb-3" role="status"></div>
        <div className="h5 text-muted animate__animated animate__pulse animate__infinite">Preparing your playground...</div>
      </div>
    </div>
  );

  const GameCard = ({ type, title, description, icon: Icon, color, gradient }) => {
    const status = gameStatus[type];
    const isLocked = status && !status.can_play;

    return (
      <Col md={4} className="mb-4">
        <div 
          className={`game-selector-card glass-card h-100 p-4 text-center d-flex flex-column align-items-center justify-content-center transition-all ${isLocked ? 'locked' : ''}`}
          onClick={() => !isLocked && setActiveGame(type)}
        >
          {isLocked && (
            <div className="locked-overlay rounded-4">
              <div className="locked-content">
                <Lock size={48} className="mb-2" />
                <span className="fw-bold d-block">LOCKED</span>
                <small className="opacity-75">Come back tomorrow!</small>
              </div>
            </div>
          )}
          <div className="icon-badge mb-4" style={{ background: gradient }}>
            <Icon size={32} color="white" />
          </div>
          <h3 className="fw-bold mb-2">{title}</h3>
          <p className="text-muted small mb-4">{description}</p>
          <Button 
            variant={isLocked ? "light" : color} 
            className="rounded-pill px-4 fw-bold shadow-sm"
            disabled={isLocked}
          >
            {isLocked ? "Play Tomorrow" : "Play Now"}
          </Button>
        </div>
      </Col>
    );
  };

  return (
    <div className="discount-games-page py-5">
      <Container>
        <div className="header-section text-center mb-5 animate__animated animate__fadeInDown">
          <Badge bg="primary-subtle" text="primary" className="px-3 py-2 rounded-pill mb-3">
            DAILY CHALLENGES
          </Badge>
          <h1 className="display-4 fw-black mb-2 text-gradient">Win Your Cookies!</h1>
          <p className="lead text-muted mx-auto" style={{ maxWidth: '600px' }}>
            Choose a game below to win exclusive discount codes. Each game can be played once per day for maximum fun!
          </p>
        </div>
        <Row>
          <Col lg={activeGame ? 8 : 12}>
            {!activeGame ? (
              <Row className="animate__animated animate__fadeInUp">
                <GameCard 
                  type="spin_wheel"
                  title="Crazy Spinner"
                  description="Spin the lucky wheel and grab up to 50% discount instantly."
                  icon={PieChart}
                  color="primary"
                  gradient="linear-gradient(135deg, #FF6B6B 0%, #FFD93D 100%)"
                />
                <GameCard 
                  type="scratch_card"
                  title="Elite Scratch"
                  description="Match 3 symbols under the gold to reveal your hidden treasure."
                  icon={Sparkles}
                  color="warning"
                  gradient="linear-gradient(135deg, #6BCB77 0%, #4D96FF 100%)"
                />
                <GameCard 
                  type="memory_match"
                  title="Cookie Memory"
                  description="Master your focus! Match all cookie pairs to win 40% off."
                  icon={Layout}
                  color="info"
                  gradient="linear-gradient(135deg, #9747FF 0%, #FF4DE8 100%)"
                />
              </Row>
            ) : (
              <div className="game-stage glass-card p-5 mb-4 animate__animated animate__zoomIn">
                <Button 
                  variant="link" 
                  className="mb-4 text-muted p-0 d-flex align-items-center text-decoration-none hover-primary"
                  onClick={() => setActiveGame(null)}
                >
                  <ArrowLeft className="me-2" size={18} /> Exit Game
                </Button>

                {activeGame === 'spin_wheel' && (
                  <div className="text-center">
                    <h2 className="fw-bold mb-4">Spin the Wheel</h2>
                    <div className="wheel-wrapper mx-auto mb-5">
                      <div className={`wheel-circle ${wheelSpinning ? 'spinning' : ''}`}>
                        {wheelDiscounts.map((d, i) => (
                          <div key={i} className="wheel-slice" style={{ '--slice-index': i }}>
                            <span>{d}%</span>
                          </div>
                        ))}
                      </div>
                      <div className="wheel-hub"></div>
                      <div className="wheel-pin"></div>
                    </div>
                    <Button 
                      size="lg" 
                      variant="primary" 
                      className="px-5 rounded-pill fw-bold shadow-lg py-3 translate-y-pulse"
                      onClick={spinWheel} 
                      disabled={wheelSpinning}
                    >
                      {wheelSpinning ? 'SPINNING...' : 'SPIN NOW'}
                    </Button>
                  </div>
                )}

                {activeGame === 'scratch_card' && (
                  <div className="text-center">
                    <h2 className="fw-bold mb-2">Scratch & Match</h2>
                    <p className="text-muted mb-4">Reveal 9 tiles. Get 3 matching values to win!</p>
                    <div className="scratch-grid-wrap mx-auto">
                      <Row className="g-3">
                        {scratchCards.map((card, i) => (
                          <Col xs={4} key={i}>
                            <div 
                              className={`scratch-tile-btn position-relative rounded-4 cursor-pointer ${card.revealed ? 'revealed' : ''}`}
                              onClick={() => revealCard(i)}
                            >
                              <div className="tile-surface">
                                <Sparkles className="shine-effect" />
                              </div>
                              <div className="tile-content">
                                <span className="val">{card.discount}%</span>
                                <span className="lab">OFF</span>
                              </div>
                            </div>
                          </Col>
                        ))}
                      </Row>
                    </div>
                    <Button 
                      variant="outline-primary" 
                      className="mt-5 rounded-pill px-4"
                      onClick={resetScratchGame}
                      disabled={scratchGameWon || (gameStatus.scratch_card && !gameStatus.scratch_card.can_play)}
                    >
                      Reset Board
                    </Button>
                  </div>
                )}

                {activeGame === 'memory_match' && (
                  <div className="text-center">
                    <h2 className="fw-bold mb-2">Cookie Memory</h2>
                    <p className="text-muted mb-4">Progress: <span className="text-primary fw-bold">{memoryMatches}/4 Matches</span></p>
                    <div className="memory-grid-wrap mx-auto">
                      <Row className="g-3">
                        {memoryCards.map((card, i) => (
                          <Col xs={3} key={card.id}>
                            <div 
                              className={`memory-card-btn ${card.flipped || card.matched ? 'flipped' : ''}`}
                              onClick={() => flipMemoryCard(i)}
                            >
                              <div className="card-face card-front">
                                <div className="card-pattern"></div>
                                <Gift size={24} className="text-white opacity-50" />
                              </div>
                              <div className="card-face card-back">
                                {card.icon}
                              </div>
                            </div>
                          </Col>
                        ))}
                      </Row>
                    </div>
                    <Button 
                      variant="outline-info" 
                      className="mt-5 rounded-pill px-4"
                      onClick={resetMemoryGame}
                      disabled={memoryMatches === 4 || (gameStatus.memory_match && !gameStatus.memory_match.can_play)}
                    >
                      Shuffle Cards
                    </Button>
                  </div>
                )}
              </div>
            )}
          </Col>

          {activeGame && (
            <Col lg={4} className="animate__animated animate__fadeInRight">
              <div className="rewards-sidebar glass-card p-4 sticky-top" style={{ top: '5rem' }}>
                <h4 className="fw-bold mb-4 d-flex align-items-center">
                  <Trophy size={20} className="me-2 text-warning" /> My Rewards
                </h4>
                {userDiscounts.length === 0 ? (
                  <div className="text-center py-5 rounded-4 bg-light bg-opacity-50 border border-dashed">
                    <Gift size={32} className="text-muted mb-2 opacity-50" />
                    <p className="text-muted small mb-0">Play a game to start your collection!</p>
                  </div>
                ) : (
                  <div className="reward-stack custom-scrollbar" style={{ maxHeight: '60vh', overflowY: 'auto' }}>
                    {userDiscounts.map((discount) => (
                      <div key={discount.id} className="reward-card mb-3 p-3 animate__animated animate__fadeInRight">
                        <div className="d-flex justify-content-between align-items-center mb-2">
                          <Badge bg="success-subtle" className="text-success text-capitalize border border-success-subtle">
                            {discount.game_type.replace('_', ' ')}
                          </Badge>
                          <span className="fw-black text-success h5 mb-0">{discount.discount_percentage}%</span>
                        </div>
                        <div className="d-flex align-items-center gap-2 bg-white p-2 rounded-3 border">
                          <code className="text-dark small flex-grow-1">{discount.code}</code>
                          <Button 
                            variant="link" 
                            className="p-1 text-primary hover-scale"
                            onClick={() => {
                              navigator.clipboard.writeText(discount.code);
                              alert('Copied!');
                            }}
                          >
                            <Copy size={16} />
                          </Button>
                        </div>
                        <div className="text-muted extra-small mt-2 d-flex justify-content-between">
                          <span>30 days left</span>
                          <span>Valid for all cookies</span>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </Col>
          )}
        </Row>
      </Container>

      {/* WINNER MODAL */}
      <Modal 
        show={showModal} 
        onHide={() => setShowModal(false)} 
        centered 
        contentClassName="border-0 bg-transparent"
        className="winner-modal"
      >
        <Modal.Body className="p-0">
          <div className="winner-card glass-card text-center p-5 overflow-hidden">
            <div className={`status-icon mb-4 ${modalDiscount > 0 ? 'win' : 'lose'}`}>
              {modalDiscount > 0 ? '🏆' : '😅'}
            </div>
            <h2 className="fw-black mb-3">{modalDiscount > 0 ? 'TA-DA! WINNER' : 'ALMOST THERE!'}</h2>
            <p className="text-muted mb-4">{modalMessage}</p>
            
            {modalDiscount > 0 && (
              <div className="discount-seal-badge mb-4 mx-auto">
                <div className="seal-inner">
                  <span className="h1 mb-0 fw-black">{modalDiscount}%</span>
                  <span className="small fw-bold">OFFER</span>
                </div>
              </div>
            )}

            <div className="d-grid gap-2">
              <Button 
                variant="primary" 
                size="lg" 
                className="rounded-pill py-3 fw-bold shadow-lg"
                onClick={() => setShowModal(false)}
              >
                {modalDiscount > 0 ? 'COLLECT REWARD' : 'TRY ANOTHER GAME'}
              </Button>
              {modalDiscount > 0 && (
                <Button 
                  variant="link" 
                  className="text-muted text-decoration-none mt-2"
                  onClick={() => setShowModal(false)}
                >
                  I want to play more!
                </Button>
              )}
            </div>
          </div>
        </Modal.Body>
      </Modal>

    </div>
  );
};

export default DiscountGamesPage;
