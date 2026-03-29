import api from '../api';

const discountService = {
  getMyDiscounts: async () => {
    return await api.get('discounts/my-discounts/');
  },
  
  claimDiscount: async (gameType, discount) => {
    return await api.post('discounts/claim/', {
      game_type: gameType,
      discount: discount
    });
  },
  
  validateDiscount: async (code) => {
    return await api.post('discounts/validate/', { code });
  },
  
  getGameStatus: async () => {
    return await api.get('discounts/status/');
  }
};

export default discountService;
